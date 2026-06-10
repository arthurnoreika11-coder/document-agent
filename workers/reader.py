from pathlib import Path
from docx import Document
from pdfminer.high_level import extract_text

class FileTypeError(ValueError):
    pass

def read_txt_file(fileName) -> str:
    file = Path(fileName).read_text()
    return file

def read_docx_file(fileName) -> str:
    doc = Document(fileName)
    fullText = []
    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        fullText.append({
            "style": para.style.name,
            "text": para.text
        })
    return fullText

def read_pdf_file(fileName) -> str:
    text = extract_text(fileName)
    return text

def read_docx(fileName) -> list[dict[str, str]]:
    return read_docx_file(fileName)

def read_pdf(fileName) -> str:
    return read_pdf_file(fileName)

def parse_file(fileName) -> str:
    try:
        path = Path(fileName)
        suffix = path.suffix.lower()
        if suffix == '.txt':
            return read_txt_file(path)
        elif suffix == '.docx':
            return read_docx_file(path)
        elif suffix == '.pdf':
            return read_pdf_file(path)
        else:
            raise FileTypeError(f"Unsupported file type: {suffix}")
    except FileTypeError as ve:
        print(ve)
        return ""
    except Exception as e:
        print(f"Error reading file {fileName}: {e}")
        return ""