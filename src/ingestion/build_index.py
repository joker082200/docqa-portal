import json
import os
from pathlib import Path
from typing import List, Dict

import numpy as np
try:
    import faiss
except ImportError:
    # faiss-cpu の場合
    from faiss import swigfaiss as faiss

from src.config import VECTORSTORE_DIR, FAISS_INDEX_PATH, FAISS_META_PATH, RAW_DATA_DIR
from src.ingestion.load_docs import load_all_docs
from src.ingestion.split_docs import simple_split
from src.models.embedder import get_embedding


def build_index() -> None:
    print("[build_index] loading documents...")
    docs = load_all_docs(str(RAW_DATA_DIR))

    texts: List[str] = []
    metadatas: List[Dict] = []

    for doc in docs:
        chunks = simple_split(doc["text"])
        for idx, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append(
                {
                    "source": doc["path"],
                    "chunk_id": idx,
                }
            )

    print(f"[build_index] total chunks: {len(texts)}")
    
    if len(texts) == 0:
        print("[build_index] No documents found. Please add markdown files to data/raw/")
        return

    print("[build_index] creating embeddings...")
    embeddings_list = []
    for i, t in enumerate(texts):
        if i % 10 == 0:  # 10件ごとに進捗表示
            print(f"  progress: {i}/{len(texts)} ({i*100//len(texts)}%)")
        embeddings_list.append(get_embedding(t))
    
    embeddings = np.array(embeddings_list, dtype="float32")
    dim = embeddings.shape[1]
    print(f"  completed: {len(texts)}/{len(texts)} (100%)")

    print("[build_index] building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    Path(VECTORSTORE_DIR).mkdir(parents=True, exist_ok=True)

    # FAISSは日本語パスを扱えないため、一時的に作業ディレクトリを変更
    original_dir = os.getcwd()
    try:
        # vectorstoreディレクトリに移動
        os.chdir(VECTORSTORE_DIR)
        # 相対パスで保存
        faiss.write_index(index, "index.faiss")
    finally:
        # 元のディレクトリに戻る
        os.chdir(original_dir)
    
    with open(FAISS_META_PATH, "w", encoding="utf-8") as f:
        json.dump({"texts": texts, "metadatas": metadatas}, f, ensure_ascii=False, indent=2)

    print("[build_index] done.")


if __name__ == "__main__":
    build_index()