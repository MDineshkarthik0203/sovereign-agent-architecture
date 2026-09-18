from .retriever import retrieve_documents

from .generator import generate_answer

from .web_search import web_search


def ask_rag(
    query,
    filters=None,
    web_permission_granted=False,
    needs_web_permission=False
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
            "web_results": [],
            "needs_web_permission": False
        }


    # =========================
    # LOCAL KNOWLEDGE MISSING
    # =========================

    # Case 1: Web permission explicitly granted by user
    if web_permission_granted:

        web_results = web_search(
            query
        )

        if not web_results:

            return {
                "status": "missing_knowledge",
                "source": "none",
                "answer": (
                    "The requested information was not found in the local knowledge base, "
                    "and external web search returned no results."
                ),
                "evidence": [],
                "web_results": [],
                "needs_web_permission": False
            }

        web_evidence = []
        for item in web_results:
            web_evidence.append({
                "document": item.get("title", "Web Search Result"),
                "page": 1,
                "section": item.get("url", "External Web"),
                "content": item.get("content", ""),
                "source_type": "web"
            })

        answer = generate_answer(
            query,
            web_evidence
        )

        labeled_answer = (
            f"{answer}\n\n"
            "Source: web search (user-approved), not local knowledge base."
        )

        return {
            "status": "success",
            "source": "web",
            "answer": labeled_answer,
            "evidence": web_evidence,
            "web_results": web_results,
            "needs_web_permission": False
        }

    # Case 2: User previously prompted and denied permission
    if needs_web_permission:

        return {
            "status": "permission_denied",
            "source": "none",
            "answer": (
                "The requested information was not found in the local knowledge base, "
                "and external web search was not permitted. No external search was performed."
            ),
            "evidence": [],
            "web_results": [],
            "needs_web_permission": False
        }

    # Case 3: First time encountering missing knowledge -> ask user for permission
    return {
        "status": "needs_permission",
        "source": "none",
        "answer": (
            "I couldn't find this in our local knowledge base. "
            "Would you like me to search the internet for this instead? "
            "(This will send your query outside the organization's local network.)"
        ),
        "evidence": [],
        "web_results": [],
        "needs_web_permission": True
    }