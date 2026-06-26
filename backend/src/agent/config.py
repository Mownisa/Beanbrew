import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.settings import config

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

def get_llm(max_tokens: int = 1000, temperature: float = 0.0):
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=config.GEMINI_API_KEY,
        max_output_tokens=max_tokens,
        temperature=temperature,
    )
