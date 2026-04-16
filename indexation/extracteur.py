import os
from pathlib import Path


def extract_text(filepath):
    ext = Path(filepath).suffix.lower()

    if ext == ".pdf":
        import PyPDF2
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif ext == ".html":
        from html.parser import HTMLParser
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.result = []

            def handle_data(self, data):
                self.result.append(data)

        parser = TextExtractor()
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            parser.feed(f.read())
        return " ".join(parser.result)

    elif ext == ".docx":
        import docx
        doc = docx.Document(filepath)
        return " ".join(p.text for p in doc.paragraphs)

    return ""