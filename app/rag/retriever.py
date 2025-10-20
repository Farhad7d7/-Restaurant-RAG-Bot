from typing import List
from rank_bm25 import BM25Okapi
from langchain_community.docstore.document import Document
from app.rag.vector_store import build_or_load_faiss, load_docs
from app.core.config import cfg

def hybrid_retrieve(query: str, k: int | None = None) -> List[Document]:
    if k is None:
        k = cfg.VECTOR_K

    vs = build_or_load_faiss()
    vec_docs = vs.similarity_search(query, k=k)

    docs_all = load_docs()
    corpus = [d.page_content for d in docs_all]
    bm25 = BM25Okapi([c.split() for c in corpus])
    scores = bm25.get_scores(query.split())
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    bm_docs = [docs_all[i] for i in top_idx]

    seen = set()
    merged: List[Document] = []
    for d in vec_docs + bm_docs:
        key = d.metadata.get("name", "") + d.page_content[:40]
        if key not in seen:
            seen.add(key)
            merged.append(d)
    return merged[:k]
