

# docqa-portal – Internal Document Q&A Bot (RAG)

社内に散在するマニュアル・FAQ・議事録などのドキュメントを対象に、

自然文で質問できるQ&Aチャットボットのプロトタイプです。


## Features

- **Markdown & PDF** ドキュメントの取り込み

- チャンク分割によるテキスト分割- Markdown ドキュメントの取り込み

- OpenAI Embedding を用いたベクトル化- チャンク分割によるテキスト分割

- FAISS による類似検索（ベクトル検索）- OpenAI Embedding を用いたベクトル化

- OpenAI Chat API による回答生成（RAG）- FAISS による類似検索（ベクトル検索）

- FastAPI による /ask エンドポイント- OpenAI Chat API による回答生成（RAG）

- Streamlit 製の簡易Web UI- FastAPI による /ask エンドポイント

- Streamlit 製の簡易Web UI



## Tech Stack

- Python 3.11+

- FastAPI / Uvicorn- Python 3.10+

- Streamlit- FastAPI / Uvicorn

- OpenAI API (Chat + Embedding)- Streamlit

- FAISS (faiss-cpu)- OpenAI API (Chat + Embedding)

- pypdf (PDF処理)- FAISS (faiss-cpu)

- python-dotenv- python-dotenv



## Setup## Setup



### 1. Clone the repository```bash

pip install -r requirements.txt

```bashcp .env.example .env  # APIキーを設定

git clone <your-repo-url>```

cd docqa-portal

````.env` に OpenAI API キーを設定します。



### 2. Create virtual environment```env

OPENAI_API_KEY=your_api_key_here

```bash```

python -m venv .venv

## Build index

# Windows PowerShell

.\.venv\Scripts\Activate.ps1```bash

python -m src.ingestion.build_index

# Mac/Linux```

source .venv/bin/activate

````data/raw/` 配下の `.md` ファイルからベクトルインデックスを生成します。



### 3. Install dependencies## Run API



```bash```bash

pip install -r requirements.txtuvicorn src.api.main:app --reload

``````



### 4. Set up environment variables## Run UI



```bash```bash

cp .env.example .envstreamlit run src.ui.app.py

``````



`.env` に OpenAI API キーを設定します。ブラウザで `http://localhost:8501` を開くと Q&A UI にアクセスできます。



```env## Project Structure

OPENAI_API_KEY=your-openai-api-key-here

``````bash

docqa-portal/

### 5. Prepare documents├─ README.md

├─ requirements.txt

`data/raw/` ディレクトリに処理したいMarkdownファイル（`.md`）またはPDFファイル（`.pdf`）を配置します。├─ .env.example

├─ docs/

## Build index│   └─ design.md

├─ data/

ドキュメントからベクトルインデックスを作成します：│   ├─ raw/

│   └─ processed/

```bash├─ vectorstore/

# Windows│   └─ index/

.\.venv\Scripts\python.exe -m src.ingestion.build_index├─ src/

│   ├─ config.py

# Mac/Linux│   ├─ models/

python -m src.ingestion.build_index│   │   └─ embedder.py

```│   ├─ ingestion/

│   │   ├─ load_docs.py

`data/raw/` 配下の `.md` および `.pdf` ファイルからベクトルインデックスを生成し、│   │   ├─ split_docs.py

`data/vectorstore/` に保存します。│   │   └─ build_index.py

│   ├─ rag/

**注意**: 602チャンク程度で10〜20分程度かかります。進捗状況が表示されます。│   │   ├─ retriever.py

│   │   └─ qa_chain.py

## Run API│   ├─ api/

│   │   └─ main.py

FastAPI サーバーを起動します：│   └─ ui/

│       └─ app.py

```bash└─ scripts/

# Windows    ├─ ingest_all.sh

.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload    └─ run_app.sh

```

# Mac/Linux```

uvicorn src.api.main:app --reload

```---



API は `http://localhost:8000` で利用可能になります。## File: requirements.txt



## Run UI```txt

fastapi

Streamlit UI を起動します：uvicorn

streamlit

```bashopenai

# Windowspython-dotenv

.\.venv\Scripts\streamlit.exe run src/ui/app.pyfaiss-cpu

tiktoken

# Mac/Linuxpydantic

streamlit run src/ui/app.pyrequests

``````



ブラウザで `http://localhost:8501` を開くと Q&A UI にアクセスできます。---



## Project Structure## File: .env.example



``````env

docqa-portal/OPENAI_API_KEY=your_api_key_here

├─ README.md```

├─ requirements.txt

├─ .env.example---

├─ .gitignore

├─ docs/## File: docs/design.md
│   └─ design.md
├─ data/
│   ├─ raw/              # ドキュメント配置場所 (.md, .pdf)
│   └─ vectorstore/      # 生成されたインデックス
│       ├─ index.faiss
│       └─ metadata.json
├─ src/
│   ├─ config.py
│   ├─ models/
│   │   ├─ embedder.py
│   │   └─ llm_client.py
│   ├─ ingestion/
│   │   ├─ load_docs.py
│   │   ├─ split_docs.py
│   │   └─ build_index.py
│   ├─ rag/
│   │   ├─ retriever.py
│   │   └─ qa_chain.py
│   ├─ api/
│   │   └─ main.py
│   └─ ui/
│       └─ app.py
└─ scripts/
    ├─ ingest_all.sh
    └─ run_app.sh
```

## Troubleshooting

### 日本語パスの問題

FAISSライブラリは日本語を含むパスを扱えないため、プロジェクトでは作業ディレクトリを一時的に変更する回避策を実装しています。

### 仮想環境の問題

`venv` と `.venv` が混在している場合は、`.venv` のみを使用してください：

```bash
# 古い venv を削除（任意）
rm -rf venv  # Mac/Linux
Remove-Item -Recurse -Force venv  # Windows PowerShell
```

## License

MIT
