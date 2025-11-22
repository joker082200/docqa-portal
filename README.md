![CI](https://github.com/joker082200/docqa-portal/actions/workflows/python-ci.yml/badge.svg)

# docqa-portal



[English](#english) | [日本語](#japanese)# docqa-portal – Internal Document Q&A Bot (RAG)



---社内に散在するマニュアル・FAQ・議事録などのドキュメントを対象に、



<a name="english"></a>自然文で質問できるQ&Aチャットボットのプロトタイプです。

## 🇬🇧 English



### Internal Document Q&A Bot (RAG)## Features



A prototype chatbot that enables natural language queries across internal documents such as manuals, FAQs, and meeting minutes using Retrieval-Augmented Generation (RAG).- **Markdown & PDF** ドキュメントの取り込み



### ✨ Features- チャンク分割によるテキスト分割- Markdown ドキュメントの取り込み



- 📄 **Document Support**: Markdown (`.md`) and PDF (`.pdf`) files- OpenAI Embedding を用いたベクトル化- チャンク分割によるテキスト分割

- 🔪 **Smart Chunking**: Text splitting for optimal vector search

- 🧠 **Vector Embeddings**: OpenAI Embedding API integration- FAISS による類似検索（ベクトル検索）- OpenAI Embedding を用いたベクトル化

- 🔍 **Fast Search**: FAISS-powered similarity search

- 💬 **AI-Powered Answers**: OpenAI Chat API for response generation- OpenAI Chat API による回答生成（RAG）- FAISS による類似検索（ベクトル検索）

- 🚀 **REST API**: FastAPI endpoint (`/ask`)

- 🖥️ **Web UI**: Simple Streamlit-based interface- FastAPI による /ask エンドポイント- OpenAI Chat API による回答生成（RAG）



### 🛠️ Tech Stack- Streamlit 製の簡易Web UI- FastAPI による /ask エンドポイント



- **Python** 3.11+- Streamlit 製の簡易Web UI

- **FastAPI** / Uvicorn

- **Streamlit**

- **OpenAI API** (Chat + Embeddings)

- **FAISS** (faiss-cpu)## Tech Stack

- **pypdf** (PDF processing)

- **python-dotenv**- Python 3.11+



### 📦 Installation- FastAPI / Uvicorn- Python 3.10+



#### 1. Clone the repository- Streamlit- FastAPI / Uvicorn



```bash- OpenAI API (Chat + Embedding)- Streamlit

git clone https://github.com/joker082200/docqa-portal.git

cd docqa-portal- FAISS (faiss-cpu)- OpenAI API (Chat + Embedding)

```

- pypdf (PDF処理)- FAISS (faiss-cpu)

#### 2. Create virtual environment

- python-dotenv- python-dotenv

```bash

python -m venv .venv



# Windows PowerShell## Setup## Setup

.\.venv\Scripts\Activate.ps1



# Mac/Linux

source .venv/bin/activate### 1. Clone the repository```bash

```

pip install -r requirements.txt

#### 3. Install dependencies

```bashcp .env.example .env  # APIキーを設定

```bash

pip install -r requirements.txtgit clone <your-repo-url>```

```

cd docqa-portal

#### 4. Set up environment variables

````.env` に OpenAI API キーを設定します。

```bash

cp .env.example .env

```

### 2. Create virtual environment```env

Edit `.env` and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

```env

OPENAI_API_KEY=your-openai-api-key-here```bash```

```

python -m venv .venv

#### 5. Prepare documents

## Build index

Place your Markdown (`.md`) or PDF (`.pdf`) files in the `data/raw/` directory.

# Windows PowerShell

### 🔨 Build Index

.\.venv\Scripts\Activate.ps1```bash

Generate vector index from documents:

python -m src.ingestion.build_index

```bash

# Windows# Mac/Linux```

.\.venv\Scripts\python.exe -m src.ingestion.build_index

source .venv/bin/activate

# Mac/Linux

python -m src.ingestion.build_index````data/raw/` 配下の `.md` ファイルからベクトルインデックスを生成します。

```



This creates a FAISS index from all `.md` and `.pdf` files in `data/raw/` and saves it to `data/vectorstore/`.

### 3. Install dependencies## Run API

⏱️ **Note**: Processing ~600 chunks takes approximately 10-20 minutes. Progress is displayed during execution.



### 🚀 Run Application

```bash```bash

#### Start API Server

pip install -r requirements.txtuvicorn src.api.main:app --reload

```bash

# Windows``````

.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload



# Mac/Linux

uvicorn src.api.main:app --reload### 4. Set up environment variables## Run UI

```



API available at: `http://localhost:8000`

```bash```bash

#### Start Web UI

cp .env.example .envstreamlit run src.ui.app.py

```bash

# Windows``````

.\.venv\Scripts\streamlit.exe run src/ui/app.py



# Mac/Linux

streamlit run src/ui/app.py`.env` に OpenAI API キーを設定します。ブラウザで `http://localhost:8501` を開くと Q&A UI にアクセスできます。

```



Open your browser and navigate to: `http://localhost:8501`

```env## Project Structure

### 📂 Project Structure

OPENAI_API_KEY=your-openai-api-key-here

```

docqa-portal/``````bash

├── README.md

├── requirements.txtdocqa-portal/

├── .env.example

├── .gitignore### 5. Prepare documents├─ README.md

├── docs/

│   └── design.md├─ requirements.txt

├── data/

│   ├── raw/              # Place documents here (.md, .pdf)`data/raw/` ディレクトリに処理したいMarkdownファイル（`.md`）またはPDFファイル（`.pdf`）を配置します。├─ .env.example

│   └── vectorstore/      # Generated index files

│       ├── index.faiss├─ docs/

│       └── metadata.json

├── src/## Build index│   └─ design.md

│   ├── config.py

│   ├── models/├─ data/

│   │   ├── embedder.py

│   │   └── llm_client.pyドキュメントからベクトルインデックスを作成します：│   ├─ raw/

│   ├── ingestion/

│   │   ├── load_docs.py│   └─ processed/

│   │   ├── split_docs.py

│   │   └── build_index.py```bash├─ vectorstore/

│   ├── rag/

│   │   ├── retriever.py# Windows│   └─ index/

│   │   └── qa_chain.py

│   ├── api/.\.venv\Scripts\python.exe -m src.ingestion.build_index├─ src/

│   │   └── main.py

│   └── ui/│   ├─ config.py

│       └── app.py

└── scripts/# Mac/Linux│   ├─ models/

    ├── ingest_all.sh

    └── run_app.shpython -m src.ingestion.build_index│   │   └─ embedder.py

```

```│   ├─ ingestion/

### 🐛 Troubleshooting

│   │   ├─ load_docs.py

#### Japanese Path Issue

`data/raw/` 配下の `.md` および `.pdf` ファイルからベクトルインデックスを生成し、│   │   ├─ split_docs.py

FAISS library cannot handle paths containing Japanese characters. This project implements a workaround by temporarily changing the working directory.

`data/vectorstore/` に保存します。│   │   └─ build_index.py

#### Virtual Environment Conflicts

│   ├─ rag/

If both `venv` and `.venv` exist, use only `.venv`:

**注意**: 602チャンク程度で10〜20分程度かかります。進捗状況が表示されます。│   │   ├─ retriever.py

```bash

# Remove old venv (optional)│   │   └─ qa_chain.py

rm -rf venv  # Mac/Linux

Remove-Item -Recurse -Force venv  # Windows PowerShell## Run API│   ├─ api/

```

│   │   └─ main.py

### 📝 License

FastAPI サーバーを起動します：│   └─ ui/

MIT

│       └─ app.py

---

```bash└─ scripts/

<a name="japanese"></a>

## 🇯🇵 日本語# Windows    ├─ ingest_all.sh



### 社内ドキュメントQ&Aボット（RAG）.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload    └─ run_app.sh



社内に散在するマニュアル・FAQ・議事録などのドキュメントを対象に、自然文で質問できるQ&Aチャットボットのプロトタイプです。```



### ✨ 機能# Mac/Linux```



- 📄 **ドキュメント対応**: Markdown（`.md`）とPDF（`.pdf`）ファイルuvicorn src.api.main:app --reload

- 🔪 **スマートチャンク分割**: ベクトル検索に最適なテキスト分割

- 🧠 **ベクトル埋め込み**: OpenAI Embedding API統合```---

- 🔍 **高速検索**: FAISSによる類似度検索

- 💬 **AI回答生成**: OpenAI Chat APIによる回答生成

- 🚀 **REST API**: FastAPIエンドポイント（`/ask`）

- 🖥️ **Web UI**: Streamlit製の簡易インターフェースAPI は `http://localhost:8000` で利用可能になります。## File: requirements.txt



### 🛠️ 技術スタック



- **Python** 3.11+## Run UI```txt

- **FastAPI** / Uvicorn

- **Streamlit**fastapi

- **OpenAI API**（Chat + Embeddings）

- **FAISS**（faiss-cpu）Streamlit UI を起動します：uvicorn

- **pypdf**（PDF処理）

- **python-dotenv**streamlit



### 📦 インストール```bashopenai



#### 1. リポジトリのクローン# Windowspython-dotenv



```bash.\.venv\Scripts\streamlit.exe run src/ui/app.pyfaiss-cpu

git clone https://github.com/joker082200/docqa-portal.git

cd docqa-portaltiktoken

```

# Mac/Linuxpydantic

#### 2. 仮想環境の作成

streamlit run src/ui/app.pyrequests

```bash

python -m venv .venv``````



# Windows PowerShell

.\.venv\Scripts\Activate.ps1

ブラウザで `http://localhost:8501` を開くと Q&A UI にアクセスできます。---

# Mac/Linux

source .venv/bin/activate

```

## Project Structure## File: .env.example

#### 3. 依存関係のインストール



```bash

pip install -r requirements.txt``````env

```

docqa-portal/OPENAI_API_KEY=your_api_key_here

#### 4. 環境変数の設定

├─ README.md```

```bash

cp .env.example .env├─ requirements.txt

```

├─ .env.example---

`.env`ファイルを編集し、OpenAI APIキーを設定:

├─ .gitignore

```env

OPENAI_API_KEY=your-openai-api-key-here├─ docs/## File: docs/design.md

```│   └─ design.md

├─ data/

#### 5. ドキュメントの準備│   ├─ raw/              # ドキュメント配置場所 (.md, .pdf)

│   └─ vectorstore/      # 生成されたインデックス

`data/raw/`ディレクトリにMarkdown（`.md`）またはPDF（`.pdf`）ファイルを配置します。│       ├─ index.faiss

│       └─ metadata.json

### 🔨 インデックス作成├─ src/

│   ├─ config.py

ドキュメントからベクトルインデックスを生成:│   ├─ models/

│   │   ├─ embedder.py

```bash│   │   └─ llm_client.py

# Windows│   ├─ ingestion/

.\.venv\Scripts\python.exe -m src.ingestion.build_index│   │   ├─ load_docs.py

│   │   ├─ split_docs.py

# Mac/Linux│   │   └─ build_index.py

python -m src.ingestion.build_index│   ├─ rag/

```│   │   ├─ retriever.py

│   │   └─ qa_chain.py

`data/raw/`配下の全ての`.md`および`.pdf`ファイルからFAISSインデックスを作成し、`data/vectorstore/`に保存します。│   ├─ api/

│   │   └─ main.py

⏱️ **注意**: 約600チャンクの処理に10〜20分程度かかります。進捗状況が表示されます。│   └─ ui/

│       └─ app.py

### 🚀 アプリケーション起動└─ scripts/

    ├─ ingest_all.sh

#### APIサーバーの起動    └─ run_app.sh

```

```bash

# Windows## Troubleshooting

.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload

### 日本語パスの問題

# Mac/Linux

uvicorn src.api.main:app --reloadFAISSライブラリは日本語を含むパスを扱えないため、プロジェクトでは作業ディレクトリを一時的に変更する回避策を実装しています。

```

### 仮想環境の問題

APIは`http://localhost:8000`で利用可能です。

`venv` と `.venv` が混在している場合は、`.venv` のみを使用してください：

#### Web UIの起動

```bash

```bash# 古い venv を削除（任意）

# Windowsrm -rf venv  # Mac/Linux

.\.venv\Scripts\streamlit.exe run src/ui/app.pyRemove-Item -Recurse -Force venv  # Windows PowerShell

```

# Mac/Linux

streamlit run src/ui/app.py## License

```

MIT

ブラウザで`http://localhost:8501`を開いてください。

### 📂 プロジェクト構成

```
docqa-portal/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
│   └── design.md
├── data/
│   ├── raw/              # ドキュメント配置場所（.md, .pdf）
│   └── vectorstore/      # 生成されたインデックス
│       ├── index.faiss
│       └── metadata.json
├── src/
│   ├── config.py
│   ├── models/
│   │   ├── embedder.py
│   │   └── llm_client.py
│   ├── ingestion/
│   │   ├── load_docs.py
│   │   ├── split_docs.py
│   │   └── build_index.py
│   ├── rag/
│   │   ├── retriever.py
│   │   └── qa_chain.py
│   ├── api/
│   │   └── main.py
│   └── ui/
│       └── app.py
└── scripts/
    ├── ingest_all.sh
    └── run_app.sh
```

### 🐛 トラブルシューティング

#### 日本語パスの問題

FAISSライブラリは日本語を含むパスを扱えないため、プロジェクトでは作業ディレクトリを一時的に変更する回避策を実装しています。

#### 仮想環境の競合

`venv`と`.venv`が混在している場合は、`.venv`のみを使用してください:

```bash
# 古いvenvを削除（任意）
rm -rf venv  # Mac/Linux
Remove-Item -Recurse -Force venv  # Windows PowerShell
```

### 📝 ライセンス

MIT
