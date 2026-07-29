# Document Agent

Document Agent is a small FastAPI application for uploading documents, extracting their content, converting it into Markdown, and streaming an AI-generated analysis back to the browser.

## What the app does

The workflow is:

1. A user uploads a supported document file through the web interface.
2. The server saves the file in the uploads directory.
3. The application reads the document content based on its file type.
4. The content is converted into Markdown-friendly text.
5. The Markdown is sent to an Ollama-backed AI model for analysis.
6. The response is streamed back to the browser and displayed in the results panel.

## Supported input formats

The current implementation supports:

- PDF
- DOCX
- TXT
- MD

## Project structure

- main.py: FastAPI entrypoint and upload/convert routes
- workers/reader.py: document reading logic for different file types
- workers/mdconverter.py: conversion from extracted content to Markdown
- workers/ai.py: AI streaming integration using Ollama
- templates/index.html: frontend upload form and results viewer
- static/style.css: basic styling for the UI

## Installation

Create and activate a Python virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the app

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

Then open the app in your browser at:

```text
http://127.0.0.1:8000/
```

## AI setup

The AI analysis step depends on Ollama being available locally. The app uses the `mistral` model by default in [workers/ai.py](workers/ai.py).

Make sure Ollama is installed and running before using the analysis feature.

## How the code works

### Request flow

- The browser sends a file to the `/convert` endpoint.
- The server writes the uploaded file to the uploads folder.
- The `convert_to_markdown()` function chooses the correct reader based on the file extension.
- The extracted content is converted to Markdown and streamed through the AI layer.
- The streamed chunks are returned to the UI as plain text.

### Worker modules

- reader.py extracts content from DOCX, PDF, and text files.
- mdconverter.py formats raw content into Markdown structure.
- ai.py sends the Markdown to Ollama and yields streamed responses.

## Notes

- The current implementation is intentionally simple and focuses on document ingestion and text streaming.
- Error handling is included for unsupported file types, missing files, and processing failures.
- The generated output is written to a `.md` file alongside the uploaded document in the uploads directory.

## Development notes

If you want to extend the project, the most natural next steps are:

- improve the Markdown formatting logic
- add support for more document types
- add better parsing for complex DOCX or PDF layouts
- improve the frontend to render structured results instead of plain streamed text
