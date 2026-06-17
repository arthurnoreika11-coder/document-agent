import re
from typing import Union


def apply_markdown_format(text: str, style: str) -> str:
    """Convert paragraph style to markdown formatting."""
    formatters = {
        "Heading 1": lambda t: f"# {t}\n\n",
        "Heading 2": lambda t: f"## {t}\n\n",
        "Heading 3": lambda t: f"### {t}\n\n",
        "Normal": lambda t: f"{t}\n\n",
        "List Bullet": lambda t: f"- {t}\n",
    }
    return formatters.get(style, lambda t: f"{t}\n\n")(text)


def docx_to_markdown(docx_content: list[dict[str, str]]) -> str:
    """Convert DOCX content to Markdown format.
    
    Args:
        docx_content: List of dictionaries with 'style' and 'text' keys
        
    Returns:
        Markdown formatted string
    """
    md_content = ""
    for item in docx_content:
        style = item.get("style", "").strip()
        text = item.get("text", "").strip()

        # Skip empty items
        if not text:
            continue

        # Apply markdown formatting based on style
        md_content += apply_markdown_format(text, style)

    return md_content.strip()


def is_all_caps(text: str) -> bool:
    """Check if text is in all caps (with at least one letter)."""
    return bool(re.search(r"[A-Za-z]", text)) and text == text.upper()


def format_pdf_line(line: str) -> str:
    """Format a single line from PDF content as Markdown.
    
    Args:
        line: A line of text from PDF content
        
    Returns:
        Formatted markdown string
    """
    stripped = line.strip()
    
    # Skip empty lines
    if not stripped:
        return ""
    
    # Convert labeled lines (ending with :) to bold
    if stripped.endswith(":"):
        label = stripped[:-1].strip()
        return f"**{label}**:"
    
    # Keep numbered lists as-is
    if re.match(r"^\d+\.\s+", stripped):
        return stripped
    
    # Convert bullet points to markdown format
    if re.match(r"^[-•]\s+", stripped):
        pattern = r'^[-•]\s+'
        return f"- {re.sub(pattern, '', stripped)}"
    
    # Convert all-caps lines to headings
    if is_all_caps(stripped):
        return f"## {stripped}"
    
    return stripped


def pdf_to_markdown(pdf_content: Union[str, list[dict[str, str]]]) -> str:
    """Convert PDF content to Markdown format.
    
    Args:
        pdf_content: Either a string or list of dictionaries with 'text' keys
        
    Returns:
        Markdown formatted string
    """
    # Normalize input to list format
    if isinstance(pdf_content, str):
        pdf_content = [{"text": pdf_content}]

    md_content = ""
    for item in pdf_content:
        text = item.get("text", "")
        
        # Skip None or empty text
        if not text:
            continue

        lines = text.splitlines()
        for line in lines:
            formatted = format_pdf_line(line)
            if formatted == "":
                md_content += "\n"
            else:
                md_content += f"{formatted}\n"

        md_content += "\n"

    # Clean up excessive newlines (3+ becomes 2)
    md_content = re.sub(r"\n{3,}", "\n\n", md_content)
    return md_content.strip()


def txt_to_markdown(txt_content: Union[str, list[dict[str, str]]]) -> str:
    """Convert plain text content to Markdown format.
    
    Args:
        txt_content: Either a string or list of dictionaries with 'text' keys
        
    Returns:
        Markdown formatted string
    """
    return pdf_to_markdown(txt_content)
