from sovereign_agent.inference_client import LocalLLM


def get_llm():

    return LocalLLM()


def generate_answer(
    query,
    evidence
):

    llm = get_llm()


    context_parts = []


    for item in evidence:

        context_parts.append(
            f"""
Document: {item["document"]}
Page: {item["page"]}
Section: {item["section"]}

Content:
{item["content"]}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    prompt = f"""
You are an AI assistant inside a
Sovereign Agentic AI Workbench.

Answer the user's question using ONLY
the provided document evidence.

USER QUESTION:
{query}

DOCUMENT EVIDENCE:
{context}

RULES:

1. Use only the provided evidence.
2. Do not invent information.
3. Do not use outside knowledge.
4. If the answer is not present in the evidence,
   clearly say that the information is not available
   in the provided documents.
5. Give a clear and concise answer.
6. Mention the document and page when appropriate.

ANSWER:
"""


    response = llm.invoke(
        prompt
    )


    return response.content