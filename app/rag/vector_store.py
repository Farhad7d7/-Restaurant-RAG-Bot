import os, json
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from app.rag.embedder import get_embeddings
from app.core.config import cfg

def load_docs(processed_json: str = "app/data/processed/menu_docs.json"):
    raw = json.load(open(processed_json, "r", encoding="utf-8"))
    docs = [Document(page_content=it["text"], metadata=it["meta"]) for it in raw]
    return docs

def build_or_load_faiss(processed_json: str = "app/data/processed/menu_docs.json"):
    emb = get_embeddings()
    persist = cfg.PERSIST_DIR
    idx_path = os.path.join(persist, "index.faiss")
    store_path = os.path.join(persist, "index.pkl")
    os.makedirs(persist, exist_ok=True)
    if os.path.exists(idx_path) and os.path.exists(store_path):
        return FAISS.load_local(persist, emb, allow_dangerous_deserialization=True)
    vs = FAISS.from_documents(load_docs(processed_json), emb)
    vs.save_local(persist)
    print(f"✅ FAISS index saved to {persist}")
    return vs
