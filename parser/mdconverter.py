import re

def docx_to_markdown(docx_content) -> str:
    mdContent = ""
    for item in docx_content:
        style = item.get("style", "")
        text = item.get("text", "")

        if style in ("Heading 1", "Heading 2", "Heading 3", "Normal"):
            match style:
                case "Heading 1":
                    mdContent += f"# {text}\n\n"
                case "Heading 2":
                    mdContent += f"## {text}\n\n"
                case "Heading 3":
                    mdContent += f"### {text}\n\n"
                case "Normal":
                    mdContent += f"{text}\n\n"
        elif style == "List Bullet":
            mdContent += f"- {text}\n"
        elif style == "bold":
            mdContent += f"**{text}**\n"
        elif style == "italic":
            mdContent += f"*{text}*\n"
        elif style == "underline":
            mdContent += f"__{text}__\n"

    return mdContent.strip()


def is_all_caps(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text)) and text == text.upper()


def format_pdf_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""
    if stripped.endswith(":"):
        label = stripped[:-1].strip()
        return f"**{label}**"
    if re.match(r"^\d+\.\s*", stripped):
        return stripped
    if re.match(r"^[-•]\s+", stripped):
        return f"- {re.sub(r'^[-•]\s+', '', stripped)}"
    if is_all_caps(stripped):
        return f"## {stripped}"
    return stripped


def pdf_to_markdown(pdf_content) -> str:
    mdContent = ""
    for item in pdf_content:
        text = item.get("text", "")
        if text is None:
            continue

        lines = text.splitlines()
        for line in lines:
            formatted = format_pdf_line(line)
            if formatted == "":
                mdContent += "\n"
                continue

            mdContent += f"{formatted}\n"

        mdContent += "\n"

    mdContent = re.sub(r"\n{3,}", "\n\n", mdContent)
    return mdContent.strip()