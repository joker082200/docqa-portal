import streamlit as st
import requests

st.set_page_config(page_title="docqa-portal", layout="wide")

st.title("社内ドキュメントQ&Aボット（デモ）")

api_url = st.text_input("APIエンドポイント", "http://localhost:8000/ask")
query = st.text_area("質問を入力してください")

if st.button("送信") and query:
    with st.spinner("問い合わせ中..."):
        resp = requests.post(api_url, json={"query": query})
        if resp.status_code != 200:
            st.error(f"API error: {resp.status_code} {resp.text}")
        else:
            data = resp.json()
            st.markdown("### 回答")
            st.write(data["answer"])

            st.markdown("### 参照ドキュメント")
            for i, src in enumerate(data["sources"]):
                meta = src["metadata"]
                st.write(f"- [{i}] {meta.get('source')} (chunk: {meta.get('chunk_id')})")