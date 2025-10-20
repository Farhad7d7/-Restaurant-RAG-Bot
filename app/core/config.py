from dotenv import load_dotenv
load_dotenv()

import os

class Settings:
    EMBEDDINGS_PROVIDER: str = os.getenv("EMBEDDINGS_PROVIDER", "openai")  # openai | hf
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    HF_MODEL: str = os.getenv("HF_MODEL", "intfloat/multilingual-e5-small")

    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    VECTOR_K: int = int(os.getenv("VECTOR_K", "6"))
    PERSIST_DIR: str = os.getenv("PERSIST_DIR", ".vectordb/faiss")

    API_URL: str = os.getenv("API_URL", "http://localhost:8000")

cfg = Settings()
