from openai import OpenAI
from src.config import OPENAI_API_KEY, EMBED_MODEL

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def get_embedding(text: str) -> list[float]:
    """単一テキストから埋め込みを取得する。

    長文の場合は適宜前処理で分割してから渡すことを想定。
    """
    client = get_client()
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=text,
    )
    return resp.data[0].embedding