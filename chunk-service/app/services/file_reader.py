#app/services/file_reader.py

import os
import chardet
from pypdf import PdfReader
from bs4 import BeautifulSoup
from docx import Document
import pypandoc
from app.core.config import settings

def read_text_file(path: str) -> str:
    """Try to read file in different encoding."""
    with open(path, "rb") as f:
        raw_data = f.read()

    detected = chardet.detect(raw_data)
    encoding = detected.get("encoding") or "utf-8"

    try:
        return raw_data.decode(encoding)
    except:
        return raw_data.decode("utf-8", errors="ignore")
    
def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_html(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text(separator="\n")

def read_rtf(path: str) -> str:
    return pypandoc.convert_text(
        open(path, "r", errors="ignore").read(),
        to="plain", format="rtf"
    )

def load_text_from_file(file_name: str) -> str:
    "Detects file extension, reads it and returns text."
    path = settings.files_path+file_name
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt" or ext == ".md":
        return read_text_file(path)
    
    elif ext == ".pdf":
        return read_pdf(path)
    
    elif ext == ".docx":
        return read_docx(path)

    elif ext in [".html", ".htm"]:
        return read_html(path)
    
    elif ext == ".rtf":
        return read_rtf(path)

    else:
        return read_text_file(path)