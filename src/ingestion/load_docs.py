import logging
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader

logger = logging.getLogger(__name__)


def load_markdown_docs(root: str) -> List[Dict[str, str]]:
    """
    指定されたディレクトリ配下のMarkdownファイルを読み込む。
    
    Args:
        root: ドキュメントのルートディレクトリパス
        
    Returns:
        ドキュメントのリスト。各要素は {"path": ファイルパス, "text": テキスト内容}
    """
    root_path = Path(root)
    docs = []
    
    for path in root_path.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
            docs.append({"path": str(path), "text": text})
            logger.debug(f"Loaded markdown: {path.name}")
        except Exception as e:
            logger.error(f"Failed to read markdown file {path}: {e}")
            
    logger.info(f"Loaded {len(docs)} markdown documents")
    return docs


def load_pdf_docs(root: str) -> List[Dict[str, str]]:
    """
    指定されたディレクトリ配下のPDFファイルを読み込む。
    
    Args:
        root: ドキュメントのルートディレクトリパス
        
    Returns:
        ドキュメントのリスト。各要素は {"path": ファイルパス, "text": テキスト内容}
    """
    root_path = Path(root)
    docs = []
    
    for path in root_path.rglob("*.pdf"):
        try:
            reader = PdfReader(str(path))
            text_parts = []
            
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    
            text = "\n".join(text_parts)
            docs.append({"path": str(path), "text": text})
            logger.debug(f"Loaded PDF: {path.name} ({len(reader.pages)} pages)")
            
        except Exception as e:
            logger.error(f"Failed to read PDF file {path}: {e}")
            
    logger.info(f"Loaded {len(docs)} PDF documents")
    return docs


def load_all_docs(root: str) -> List[Dict[str, str]]:
    """
    指定されたディレクトリ配下のMarkdownとPDFファイルを全て読み込む。
    
    Args:
        root: ドキュメントのルートディレクトリパス
        
    Returns:
        全ドキュメントのリスト。各要素は {"path": ファイルパス, "text": テキスト内容}
    """
    logger.info(f"Loading documents from {root}")
    
    markdown_docs = load_markdown_docs(root)
    pdf_docs = load_pdf_docs(root)
    
    all_docs = markdown_docs + pdf_docs
    logger.info(f"Total documents loaded: {len(all_docs)}")
    
    return all_docs
