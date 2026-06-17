from pathlib import Path
from fastapi.responses import HTMLResponse
from workers.reader import FileTypeError, read_docx, read_pdf
from workers.mdconverter import docx_to_markdown, pdf_to_markdown
from workers.ai import stream_agents
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

def convert_to_markdown(input_path: str, output_path: str) -> None:
    ext = Path(input_path).suffix.lower()
    try:
        if ext == ".docx":
            content = read_docx(input_path)
            mdContent = docx_to_markdown(content)
        elif ext == ".pdf":
            content = read_pdf(input_path)
            mdContent = pdf_to_markdown(content)
        else:
            print(f"Unsupported file type: {ext}")
            return

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(mdContent)

        print(f"Markdown file created at: {output_path}")
    except FileTypeError:
        print(f"Unsupported file type: {ext}")
    except FileNotFoundError:
        print(f"File not found: {input_path}")
    except Exception as e:
        print(f"Error processing file: {e}")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})