from pathlib import Path
from typing import Iterator

from fastapi.responses import HTMLResponse, StreamingResponse
from workers.reader import FileTypeError, read_docx, read_pdf
from workers.mdconverter import docx_to_markdown, pdf_to_markdown
from workers.ai import stream_agents
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


def convert_to_markdown(input_path: str, output_path: str) -> Iterator[str]:
    ext = Path(input_path).suffix.lower()
    try:
        if ext == ".docx":
            content = read_docx(input_path)
            md_content = docx_to_markdown(content)
        elif ext == ".pdf":
            content = read_pdf(input_path)
            md_content = pdf_to_markdown(content)
        else:
            yield "Unsupported file type"
            return

        full_text: list[str] = []
        for chunk in stream_agents(md_content):
            if chunk:
                full_text.append(chunk)
                yield chunk

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("".join(full_text))

        print(f"Markdown file created at: {output_path}")
    except FileTypeError:
        yield f"Unsupported file type: {ext}"
    except FileNotFoundError:
        yield f"File not found: {input_path}"
    except Exception as e:
        yield f"Error processing file: {e}"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert")
async def convert_document(file: UploadFile = File(...)):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    temp_path = upload_dir / file.filename
    contents = await file.read()
    with temp_path.open("wb") as handle:
        handle.write(contents)

    output_path = temp_path.with_suffix(".md")

    def stream_response():
        for chunk in convert_to_markdown(str(temp_path), str(output_path)):
            yield chunk

    return StreamingResponse(stream_response(), media_type="text/plain")