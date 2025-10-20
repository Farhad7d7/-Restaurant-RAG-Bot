from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from app.rag.retriever import hybrid_retrieve
from app.core.config import cfg

SYSTEM_PROMPT = (
    "You are a restaurant assistant. "
    "Answer ONLY using the provided menu context. "
    "If the answer is not in the context, say you don't know. "
    "Keep answers concise. Use Persian."
)

def format_context(docs) -> str:
    ctx = []
    for d in docs:
        m = d.metadata
        ctx.append(f"- {m.get('name')}: مواد({', '.join(m.get('ingredients', []))}); "
                   f"آلرژن({', '.join(m.get('allergens', []))}); "
                   f"رژیم({', '.join(m.get('diets', []))}); "
                   f"قیمت({m.get('price','?')} {m.get('currency','')})")
    return "\n".join(ctx)

def answer(query: str) -> dict:
    docs = hybrid_retrieve(query, k=cfg.VECTOR_K)
    context = format_context(docs)
    llm = ChatOpenAI(model=cfg.OPENAI_CHAT_MODEL, temperature=0.2, api_key=cfg.OPENAI_API_KEY)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT + "\n\nContext:\n" + context),
        HumanMessage(content=query),
    ]
    resp = llm.invoke(messages)
    return {"answer": resp.content, "context": context}
