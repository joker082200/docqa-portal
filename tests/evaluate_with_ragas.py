"""
RAGAS を使った RAG システムの評価スクリプト

使用方法:
    python tests/evaluate_with_ragas.py
"""

import json
import sys
from pathlib import Path
import pandas as pd

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# 独自のRAG システムをインポート
from src.rag.retriever import Retriever
from src.rag.qa_chain import answer
from src.models.embedder import get_embedding
from src.config import OPENAI_API_KEY


def load_test_data(filepath: str) -> list:
    """テストデータを読み込む"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_rag_system(question: str) -> dict:
    """
    RAGシステムを実行して回答と検索コンテキストを取得
    
    Args:
        question: ユーザーの質問
        
    Returns:
        answer: 生成された回答
        contexts: 検索されたドキュメントのリスト
    """
    # 1. クエリ埋め込みを取得
    query_embedding = get_embedding(question)
    
    # 2. Retrieverで類似ドキュメントを検索
    retriever = Retriever()
    similar_docs = retriever.query(query_embedding, k=3)
    
    # 3. コンテキストを抽出
    contexts = [doc['text'] for doc in similar_docs]
    
    # 4. qa_chainで回答を生成
    answer_text, _ = answer(question)
    
    return {
        "answer": answer_text,
        "contexts": contexts
    }


def prepare_ragas_dataset(test_cases: list) -> Dataset:
    """
    テストケースをRAGAS形式のデータセットに変換
    
    RAGAS requires:
        - question: 質問
        - answer: システムが生成した回答
        - contexts: 検索されたドキュメント（リスト）
        - ground_truth: 正解の回答（評価用）
    """
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }
    
    print("RAGシステムを実行中...")
    for i, case in enumerate(test_cases, 1):
        question = case["question"]
        ground_truth = case["ground_truth"]
        
        print(f"\n[{i}/{len(test_cases)}] 質問: {question}")
        
        # RAGシステムを実行
        result = run_rag_system(question)
        
        # データを追加
        data["question"].append(question)
        data["answer"].append(result["answer"])
        data["contexts"].append(result["contexts"])
        data["ground_truth"].append(ground_truth)
        
        print(f"  回答: {result['answer'][:100]}...")
        print(f"  検索されたコンテキスト数: {len(result['contexts'])}")
    
    # Hugging Face Dataset に変換
    return Dataset.from_dict(data)


def main():
    """メイン実行関数"""
    print("=" * 60)
    print("RAGAS による RAG システム評価")
    print("=" * 60)
    
    # 1. テストデータを読み込む
    test_data_path = project_root / "tests" / "test_data_ragas.json"
    if not test_data_path.exists():
        print(f"❌ テストデータが見つかりません: {test_data_path}")
        return
    
    test_cases = load_test_data(test_data_path)
    print(f"\n✅ テストケース数: {len(test_cases)}")
    
    # 2. RAGASデータセットを準備
    dataset = prepare_ragas_dataset(test_cases)
    
    # 3. RAGAS評価を実行
    print("\n" + "=" * 60)
    print("RAGAS 評価を実行中...")
    print("=" * 60)
    
    # 評価指標を定義（基本的なメトリクスのみ使用）
    metrics = [
        faithfulness,        # 忠実性: 回答が検索コンテキストに基づいているか
        answer_relevancy,    # 関連性: 回答が質問に関連しているか
    ]
    
    # 評価実行
    result = evaluate(
        dataset,
        metrics=metrics,
    )
    
    # 4. 結果を表示
    print("\n" + "=" * 60)
    print("評価結果")
    print("=" * 60)
    
    print("\n【総合スコア】")
    # RAGASのEvaluationResultオブジェクトから結果を取得
    result_df = result.to_pandas()
    
    # 各メトリクスの平均スコアを計算して表示
    metric_columns = ['faithfulness', 'answer_relevancy']
    for col in metric_columns:
        if col in result_df.columns:
            scores = pd.to_numeric(result_df[col], errors='coerce').dropna()
            if len(scores) > 0:
                avg_score = scores.mean()
                print(f"  {col}: {avg_score:.4f}")
    
    print("\n【スコアの解釈】")
    print("  - faithfulness (忠実性): 1.0に近いほど、回答が検索したドキュメントに忠実")
    print("  - answer_relevancy (関連性): 1.0に近いほど、回答が質問に関連している")
    print("\n  ※ 0.8以上: 良好 | 0.6-0.8: 改善の余地 | 0.6未満: 要改善")
    
    # 5. 詳細結果をファイルに保存
    output_path = project_root / "tests" / "ragas_evaluation_results.json"
    result_df = result.to_pandas()
    result_df.to_json(output_path, orient='records', force_ascii=False, indent=2)
    
    print(f"\n✅ 詳細結果を保存しました: {output_path}")


if __name__ == "__main__":
    # OpenAI APIキーの確認
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY が設定されていません")
        print("   .env ファイルに API キーを設定してください")
        sys.exit(1)
    
    main()
