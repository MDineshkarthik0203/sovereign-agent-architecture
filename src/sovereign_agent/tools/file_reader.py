import os

from pypdf import PdfReader


def read_text_file(file_path: str) -> str:
    """
    Read a plain text or Markdown file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return f"File not found: {file_path}"

    except Exception as e:
        return f"Error reading file: {str(e)}"


def read_pdf_file(file_path: str) -> str:
    """
    Read text from a PDF file.
    """

    try:
        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                pages.append(
                    f"--- Page {page_number} ---\n{text}"
                )

        if not pages:
            return "No extractable text found in the PDF."

        return "\n\n".join(pages)

    except FileNotFoundError:
        return f"File not found: {file_path}"

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def read_file(file_path: str) -> str:
    """
    Read a supported file based on its extension.

    Currently supported:
    - .txt
    - .md
    - .pdf
    """

    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".txt", ".md"]:
        return read_text_file(file_path)

    elif extension == ".pdf":
        return read_pdf_file(file_path)

    return f"Unsupported file type: {extension}"