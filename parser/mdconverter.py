import re

def docx_to_markdown(docx_content) -> str:
    mdContent = ""
    for item in docx_content:
        style = item.get("style", "")
        text = item.get("text", "")
        
        case = re.search(r"Heading\s\d", style):
        if case = "Heading 1" or case == "Heading 2" or case == "Heading 3" or case == "Normal":
            match case:
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

def pdf_to_markdown(pdf_content) -> str:
    mdContent = ""
    for item in pdf_content:
        style = item.get("style", "")
        text = item.get("text", "")

        //write regex to match pdf styles and convert to markdown
    return mdContent.strip()