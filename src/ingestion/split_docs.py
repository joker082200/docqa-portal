from typing import List


def simple_split(text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
    """単純な文字数ベースのチャンク分割。

    実運用では見出し単位や文単位の分割に置き換え可能。
    """
    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = end - overlap

    return chunks