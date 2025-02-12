import re
from openai import OpenAI
from config import Config


class QueryInterpreter:
    def __init__(self):
        self.client = OpenAI(api_key=Config.LLM_API_KEY)

    def read_prompt(self):
        with open("data/prompts/query_interpretation.txt", "r", encoding="utf-8") as file:
            return file.read()

    async def interpret_query(self, query):
        prompt = self.read_prompt().replace("{query}", query)

        completion = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            temperature=0.0,
            messages=[
                {"role": "assistant", "content": "You are a helpful assistant and expert in linguistics."},
                {"role": "user", "content": prompt},
            ],
        )

        response = completion.choices[0].message.content
        return self.extract_values(response)

    def extract_values(self, response):
        question = re.search(r'<question>(.*?)<command>', response)
        command = re.search(r'<command>(.*?)<expectation>', response)
        expectation = re.search(r'<expectation>(.*?)<end>', response)

        return {
            "question": question.group(1).strip() if question else "Not Found",
            "command": command.group(1).strip() if command else "",
            "expectation": expectation.group(1).strip() if expectation else "Not Found",
        }