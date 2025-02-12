import os

class Config:
    LLM_MODEL = "gpt-4o-mini-2024-07-18"
    LLM_API_KEY = os.getenv("GRAPHRAG_API_KEY")
    COMMUNITY_LEVEL = 2
    MAX_TOKENS = 12000
    OUTPUT_DIR = "output/"