import pandas as pd
import tiktoken
from graphrag.query.indexer_adapters import (
    read_indexer_communities,
    read_indexer_entities,
    read_indexer_reports,
)
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext
from graphrag.query.structured_search.global_search.search import GlobalSearch
from config import Config


class GlobalSearchService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config.LLM_API_KEY,
            model=Config.LLM_MODEL,
            api_type=OpenaiApiType.OpenAI,
            max_retries=20,
        )
        self.token_encoder = tiktoken.encoding_for_model(Config.LLM_MODEL)

    def load_data(self):
        self.community_df = pd.read_parquet("data/knowledge-graph/create_final_communities.parquet")
        self.nodes_df = pd.read_parquet("data/knowledge-graph/create_final_nodes.parquet")
        self.entity_df = pd.read_parquet("data/knowledge-graph/create_final_entities.parquet")
        self.report_df = pd.read_parquet("data/knowledge-graph/create_final_community_reports.parquet")

        self.communities = read_indexer_communities(
            final_communities=self.community_df,
            final_nodes=self.nodes_df,
            final_community_reports=self.report_df,
        )
        self.reports = read_indexer_reports(
            final_community_reports=self.report_df,
            final_nodes=self.nodes_df,
            community_level=Config.COMMUNITY_LEVEL,
        )
        self.entities = read_indexer_entities(
            final_nodes=self.nodes_df,
            final_entities=self.entity_df,
            community_level=Config.COMMUNITY_LEVEL,
        )

    async def global_search(self, query, response_type):
        self.load_data()
        
        context_builder = GlobalCommunityContext(
            community_reports=self.reports,
            communities=self.communities,
            entities=self.entities,
            token_encoder=self.token_encoder,
        )

        context_builder_params = {
        "use_community_summary": False,  # False means using full community reports. True means using community short summaries.
        "shuffle_data": True,
        "include_community_rank": True,
        "min_community_rank": 0,
        "community_rank_name": "rank",
        "include_community_weight": True,
        "community_weight_name": "occurrence weight",
        "normalize_community_weight": True,
        "max_tokens": 12_000,  # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
        "context_name": "Reports",
        }

        map_llm_params = {
            "max_tokens": 1000,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }

        reduce_llm_params = {
            "max_tokens": 2000,  # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 1000-1500)
            "temperature": 0,
        }

        search_engine = GlobalSearch(
        llm=self.llm,
        context_builder=context_builder,
        token_encoder=self.token_encoder,
        max_data_tokens=12_000,  # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
        map_llm_params=map_llm_params,
        reduce_llm_params=reduce_llm_params,
        allow_general_knowledge=False,  # set this to True will add instruction to encourage the LLM to incorporate general knowledge in the response, which may increase hallucinations, but could be useful in some use cases.
        json_mode=True,  # set this to False if your LLM model does not support JSON mode.
        context_builder_params=context_builder_params,
        concurrent_coroutines=32,
        response_type=response_type,
    )

        result = await search_engine.asearch(query)
        return result.response
    
    async def search(self, query_data, question_type, number_of_questions):

        question = query_data["question"]
        command = query_data["command"]
        expectation = query_data["expectation"]

        if expectation == "1":  # Direct information retrieval and generation
            response_type = f"""
            Provide {number_of_questions} {question_type} questions.
            Difficulty Level Should be suitable for students studying bachelor of science in computer science.
            For the query, output should be in given JSON FORMAT and include the HTML <JSON></JSON> tags to encapsulate your JSON output.
            Note that if the response does not follow the JSON TEMPLATE, your response will be rejected.
            Also do not provide any other text apart from the JSON OUTPUT.
            JSON TEMPLATE:
            {{JSON_TEMPLATE}}
            <JSON> 
            [
                {{"question": <This is Question 1 Text>, "options": [option 1, option 2, option 3, option 4], "correct_options": [index (starting from zero) of correct options]}}
            ]
            </JSON>
            """
            result = await self.global_search(query=question, response_type=response_type)

        elif expectation == "2":  # Fetch information first, then generate questions
            initial_result = await self.global_search(query=question, response_type="detailed information in bullet points")

            response_type = f"""
            {command}
            Provide {number_of_questions} {question_type} questions.
            Difficulty Level Should be suitable for students studying bachelor of science in computer science.
            For the query, output should be in given JSON FORMAT and include the HTML <JSON></JSON> tags to encapsulate your JSON output.
            Note that if the response does not follow the JSON TEMPLATE, your response will be rejected.
            Also do not provide any other text apart from the JSON OUTPUT.
            JSON TEMPLATE:
            {{JSON_TEMPLATE}}
            <JSON> 
            [
                {{"question": <This is Question 1 Text>, "options": [option 1, option 2, option 3, option 4], "correct_options": [index (starting from zero) of correct options]}}
            ]
            </JSON>
            """
            result = await self.global_search(query=initial_result, response_type=response_type)
        
        return result
