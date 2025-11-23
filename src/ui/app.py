import streamlit as st
import requests

st.set_page_config(page_title="docqa-portal", layout="wide")

# カスタムCSSでChatGPT風のデザイン
st.markdown("""
<style>
    .user-message {
        background-color: #f0f0f0;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 20%;
        text-align: left;
    }
    .bot-message {
        background-color: #e8f4f8;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 20%;
        text-align: left;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 8px;
        font-size: 14px;
        color: #666;
    }
    .message-content {
        font-size: 15px;
        line-height: 1.6;
        color: #333;
    }
    /* 入力欄を下部に固定風 */
    .input-container {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 20px 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("社内ドキュメントQ&Aボット（デモ）")

# --- セッション状態の初期化 ---
if "history" not in st.session_state:
    # 各要素: {"query": str, "answer": str, "sources": list[dict]}
    st.session_state.history = []

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# --- サイドバー設定 ---
with st.sidebar:
    st.markdown("### ⚙️ 設定")
    api_url = st.text_input("APIエンドポイント", "http://localhost:8000/ask")
    if st.button("🗑️ 履歴をクリア"):
        st.session_state.history = []
        st.rerun()

# --- 会話履歴の表示（上部に配置） ---
st.markdown("### 💬 会話")

if not st.session_state.history:
    st.info("👋 こんにちは！質問を入力してください。")
else:
    # 過去 → 新しい順に表示
    for i, turn in enumerate(st.session_state.history):
        # ユーザーの質問（右寄せ、グレー背景）
        st.markdown(f"""
        <div class="user-message">
            <div class="message-header">👤 あなた</div>
            <div class="message-content">{turn["query"]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ボットの回答（左寄せ、青背景）
        st.markdown(f"""
        <div class="bot-message">
            <div class="message-header">🤖 アシスタント</div>
            <div class="message-content">{turn["answer"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # 参照ドキュメント
        if turn["sources"]:
            with st.expander("📄 参照ドキュメント", expanded=False):
                for j, src in enumerate(turn["sources"]):
                    meta = src.get("metadata", {})
                    text_preview = src.get("text", "")[:120].replace("\n", " ")
                    st.markdown(
                        f"**[{j+1}]** `{meta.get('source')}` (chunk: {meta.get('chunk_id')})  \n"
                        f"> {text_preview}..."
                    )
        
        st.markdown("<br>", unsafe_allow_html=True)  # 会話間のスペース

# --- 入力エリア（下部に配置） ---
st.markdown("---")  # 区切り線

# --- 入力エリア（下部に配置） ---
st.markdown("---")  # 区切り線

query = st.text_area(
    "💭 メッセージを入力",
    value=st.session_state.current_query,
    key="query_input",
    placeholder="例：パスワードをリセットする手順を教えてください",
    height=100,
)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    send_clicked = st.button("📤 送信", use_container_width=True)
with col2:
    if st.button("🔄 リセット", use_container_width=True):
        st.session_state.current_query = ""
        st.rerun()

# --- 送信処理 ---
if send_clicked and query.strip():
    st.session_state.current_query = query
    try:
        with st.spinner("問い合わせ中..."):
            resp = requests.post(api_url, json={"query": query})
        if resp.status_code != 200:
            st.error(f"API error: {resp.status_code} {resp.text}")
        else:
            data = resp.json()
            # 履歴に追加
            st.session_state.history.append(
                {
                    "query": query,
                    "answer": data.get("answer", ""),
                    "sources": data.get("sources", []),
                }
            )
            # 入力欄をクリア（次回の再実行時に反映される）
            st.session_state.current_query = ""
            st.rerun()  # 画面を再描画して入力欄をクリア
    except Exception as e:
        st.error(f"❌ リクエスト中にエラーが発生しました: {e}")