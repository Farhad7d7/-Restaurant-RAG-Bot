from app.core.config import cfg

def get_embeddings():
    provider = cfg.EMBEDDINGS_PROVIDER.lower()
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=cfg.OPENAI_EMBED_MODEL, api_key=cfg.OPENAI_API_KEY)
    elif provider == "hf":
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=cfg.HF_MODEL)
    else:
        raise ValueError(f"Unsupported EMBEDDINGS_PROVIDER: {cfg.EMBEDDINGS_PROVIDER}")
