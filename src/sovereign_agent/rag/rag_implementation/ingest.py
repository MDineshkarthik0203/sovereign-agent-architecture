import os
import shutil

import pymupdf

from langchain_core.documents import Document
from langchain_chroma import Chroma

from .chunking import split_text
from .models import get_embeddings

from .config import (
    DOCUMENT_DIR,
    CHROMA_DIR,
    COLLECTION_NAME
)


def load_pdfs():

    documents = []

    if not os.path.exists(DOCUMENT_DIR):

        os.makedirs(
            DOCUMENT_DIR,
            exist_ok=True
        )

        print(
            f"Created document directory: {DOCUMENT_DIR}"
        )

        return documents


    for file_name in os.listdir(DOCUMENT_DIR):

        if not file_name.lower().endswith(".pdf"):
            continue


        file_path = os.path.join(
            DOCUMENT_DIR,
            file_name
        )

        print(
            f"Loading: {file_name}"
        )


        pdf = pymupdf.open(
            file_path
        )


        for page_number, page in enumerate(pdf):

            text = page.get_text()


            if not text.strip():
                continue


            chunks = split_text(
                text
            )


            for chunk in chunks:

                document = Document(
                    page_content=chunk,
                    metadata={
                        "document": file_name,
                        "page": page_number + 1,
                        "section": "Unknown",
                        "source_type": "local"
                    }
                )

                documents.append(
                    document
                )


        pdf.close()


    return documents


def create_database():

    print(
        "Starting document ingestion..."
    )


    documents = load_pdfs()


    print(
        f"Total chunks: {len(documents)}"
    )


    if not documents:

        print(
            "No PDF documents found."
        )

        return


    if os.path.exists(CHROMA_DIR):

        print(
            "Removing existing Chroma database..."
        )

        shutil.rmtree(
            CHROMA_DIR
        )


    print(
        "Creating OpenAI embeddings..."
    )


    embeddings = get_embeddings()


    print(
        "Creating Chroma database..."
    )


    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )


    print(
        "Knowledge base created successfully."
    )


if __name__ == "__main__":

    create_database()