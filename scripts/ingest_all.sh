#!/usr/bin/env bash
set -e

python -m src.ingestion.build_index
```

---

## File: scripts/run_app.sh

```bash
#!/usr/bin/env bash
set -e

# API サーバー起動
uvicorn src.api.main:app --reload &
API_PID=$!

# UI 起動
streamlit run src.ui.app.py &
UI_PID=$!

trap "kill $API_PID $UI_PID" INT
wait