from langchain_chroma import Chroma

from .models import get_embeddings

from .config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    RETRIEVAL_K,
    FINAL_K
)


embeddings = get_embeddings()


vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)


def retrieve_documents(
    query,
    filters=None
):

    documents = vectorstore.similarity_search(
        query,
        k=RETRIEVAL_K
    )


    # =========================
    # FILTERS
    # =========================

    if filters:

        filtered_documents = []


        for doc in documents:

            match = True


            for key, value in filters.items():

                if str(
                    doc.metadata.get(key)
                ) != str(value):

                    match = False

                    break


            if match:

                filtered_documents.append(
                    doc
                )


        documents = filtered_documents


    # =========================
    # NO DOCUMENTS
    # =========================

    if not documents:

        return {
            "status": "missing_knowledge",
            "query": query,
            "evidence": [],
            "message": (
                "No relevant information was found "
                "in the local knowledge base."
            )
        }


    # =========================
    # TOP DOCUMENTS
    # =========================

    documents = documents[
        :FINAL_K
    ]


    evidence = []


    for doc in documents:

        evidence.append(
            {
                "document": doc.metadata.get(
                    "document"
                ),

                "page": doc.metadata.get(
                    "page"
                ),

                "section": doc.metadata.get(
                    "section"
                ),

                "content": doc.page_content,

                "source_type": "local"
            }
        )


    return {
        "status": "success",
        "query": query,
        "evidence": evidence
    }