import json
import os
import sys
from pathlib import Path
from typing import List, Dict
import logging

# プロジェクトルートをパスに追加（VS Codeから直接実行する場合のため）
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# httpxとopenaiのログを抑制（WARNINGレベル以上のみ表示）
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


def build_index() -> None:
    logger.info("Starting index build process...")
    
    # ドキュメント読み込み（エラーハンドリング付き）
    try:
        logger.info(f"Loading documents from {RAW_DATA_DIR}")
        docs = load_all_docs(str(RAW_DATA_DIR))
        logger.info(f"Successfully loaded {len(docs)} documents")
    except FileNotFoundError:
        logger.error(f"Directory not found: {RAW_DATA_DIR}")
        logger.error("Please create data/raw/ directory and add documents")
        raise
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        raise

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

    logger.info(f"Total chunks created: {len(texts)}")
    
    if len(texts) == 0:
        logger.warning("No documents found. Please add markdown or PDF files to data/raw/")
        return

    # Embeddings作成
    logger.info("Creating embeddings...")
    embeddings_list = []
    for i, t in enumerate(texts):
        if i % 10 == 0:  # 10件ごとに進捗表示
            logger.info(f"Progress: {i}/{len(texts)} ({i*100//len(texts)}%)")
        embeddings_list.append(get_embedding(t))
    
    embeddings = np.array(embeddings_list, dtype="float32")
    dim = embeddings.shape[1]
    logger.info(f"Completed: {len(texts)}/{len(texts)} (100%)")

    # FAISSインデックス作成
    logger.info("Building FAISS index...")
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
        logger.info("FAISS index saved successfully")
    except Exception as e:
        logger.error(f"Failed to save FAISS index: {e}")
        raise
    finally:
        # 元のディレクトリに戻る
        os.chdir(original_dir)
    
    # メタデータ保存
    try:
        with open(FAISS_META_PATH, "w", encoding="utf-8") as f:
            json.dump({"texts": texts, "metadatas": metadatas}, f, ensure_ascii=False, indent=2)
        logger.info("Metadata saved successfully")
    except Exception as e:
        logger.error(f"Failed to save metadata: {e}")
        raise

    logger.info("Index build completed successfully!")



if __name__ == "__main__":
    build_index()