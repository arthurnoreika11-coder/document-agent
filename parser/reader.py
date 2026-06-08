from pathlib import Path

def read_txt_file(fileName) -> str:
    file = Path(fileName).read_text()
    return file