from typing import Tuple, List, Dict

from openai import OpenAI

from src.config import OPENAI_API_KEY, LLM_MODEL
from src.models.embedder import get_embedding
from src.rag.retriever import Retriever

client = OpenAI(api_key=OPENAI_API_KEY)
retriever = Retriever()

SYSTEM_PROMPT = """あなたは社内ドキュメントに基づいて回答するアシスタントです。
与えられたコンテキストの範囲内で回答し、分からない場合は「分かりません」と答えてください。
回答の最後に、参照したドキュメントの概要（ファイルパスなど）を列挙してください。
"""


def answer(query: str) -> Tuple[str, List[Dict]]:
    # 1. クエリ埋め込み
    q_emb = get_embedding(query)

    # 2. 類似チャンク検索
    docs = retriever.query(q_emb, k=5)

    # 3. コンテキスト組み立て
    context = "\n\n".join(
        f"[doc{i}] source={d['metadata']['source']}\n{d['text']}" for i, d in enumerate(docs)
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"質問: {query}\n\nコンテキスト:\n{context}",
        },
    ]

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
    )
    content = resp.choices[0].message.content
    return content, docs