from langchain_openai import OpenAIEmbeddings

from .config import (
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL
)


def get_embeddings():

    return OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )