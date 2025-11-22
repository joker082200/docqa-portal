import json
import os
from typing import List, Dict

import numpy as np
try:
    import faiss
except ImportError:
    # faiss-cpu の場合
    from faiss import swigfaiss as faiss

from src.config import FAISS_INDEX_PATH, FAISS_META_PATH, VECTORSTORE_DIR


class Retriever:
    def __init__(self, index_path: str = FAISS_INDEX_PATH, meta_path: str = FAISS_META_PATH) -> None:
        # FAISSは日本語パスを扱えないため、作業ディレクトリを変更して読み込む
        original_dir = os.getcwd()
        try:
            os.chdir(VECTORSTORE_DIR)
            self.index = faiss.read_index("index.faiss")
        finally:
            os.chdir(original_dir)
        
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        self.texts: List[str] = meta["texts"]
        self.metadatas: List[Dict] = meta["metadatas"]

    def query(self, query_embedding: list[float], k: int = 5) -> List[Dict]:
        """クエリ埋め込みに近いチャンクを上位k件返す。"""
        vec = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(vec, k)

        results: List[Dict] = []
        for idx in indices[0]:
            results.append(
                {
                    "text": self.texts[idx],
                    "metadata": self.metadatas[idx],
                }
            )
        return results