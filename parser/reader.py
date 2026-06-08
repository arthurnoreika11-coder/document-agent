from pathlib import Path

def read_txt_file(fileName):
    file = Path(fileName).read_text()
    return file