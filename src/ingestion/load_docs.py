from pathlib import Path
from pypdf import PdfReader

def load_markdown_docs(root: str):
    root_path = Path(root)
    docs = []
    for path in root_path.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        docs.append({"path": str(path), "text": text})
    return docs


def load_pdf_docs(root: str):
    root_path = Path(root)
    docs = []
    for path in root_path.rglob("*.pdf"):
        try:
            reader = PdfReader(str(path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            docs.append({"path": str(path), "text": text})
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return docs


def load_all_docs(root: str):
    """Load both markdown and PDF documents from the root directory."""
    docs = []
    docs.extend(load_markdown_docs(root))
    docs.extend(load_pdf_docs(root))
    return docs
