from .retriever import retrieve_documents

from .generator import generate_answer

from .web_search import web_search


def ask_rag(
    query,
    filters=None,
    allow_web_fallback=True
):

    # =========================
    # LOCAL KNOWLEDGE SEARCH
    # =========================

    result = retrieve_documents(
        query,
        filters=filters
    )


    # =========================
    # LOCAL KNOWLEDGE FOUND
    # =========================

    if result["status"] == "success":

        answer = generate_answer(
            query,
            result["evidence"]
        )


        return {
            "status": "success",

            "source": "local",

            "answer": answer,

            "evidence": result["evidence"],

            "web_results": []
        }


    # =========================
    # WEB FALLBACK DISABLED
    # =========================

    if not allow_web_fallback:

        return {
            "status": "missing_knowledge",

            "source": "none",

            "answer": (
                "The requested information was not "
                "found in the local knowledge base."
            ),

            "evidence": [],

            "web_results": []
        }


    # =========================
    # WEB SEARCH
    # =========================

    web_results = web_search(
        query
    )


    if not web_results:

        return {
            "status": "missing_knowledge",

            "source": "none",

            "answer": (
                "The information was not found in "
                "the local knowledge base or web search."
            ),

            "evidence": [],

            "web_results": []
        }


    return {
        "status": "success",

        "source": "web",

        "answer": (
            "The information was not found in the "
            "local knowledge base. Web search results "
            "are available."
        ),

        "evidence": [],

        "web_results": web_results
    }