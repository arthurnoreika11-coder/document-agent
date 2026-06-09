from pathlib import Path
from parser.reader import FileTypeError, read_docx, read_pdf
from parser.mdconverter import docx_to_markdown, pdf_to_markdown

def convert_to_markdown(input_path: str, output_path: str) -> None:
    ext = Path(input_path).suffix.lower()
    try:
        if ext == ".docx":
            content = read_docx(inputPath)
            mdContent = docx_to_markdown(content)
        elif ext == ".pdf":
            content = read_pdf(inputPath)
            mdContent = pdf_to_markdown(content)
        else:
            print(f"Unsupported file type: {ext}")
            return

        with open(outputPath, "w", encoding="utf-8") as f:
            f.write(mdContent)

        print(f"Markdown file created at: {outputPath}")
    except FileTypeError:
        print(f"Unsupported file type: {ext}")
    except FileNotFoundError:
        print(f"File not found: {inputPath}")
    except Exception as e:
        print(f"Error processing file: {e}")