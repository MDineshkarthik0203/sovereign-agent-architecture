from sovereign_agent.rag.rag_implementation.rag import ask_rag


query = "What is the purpose of the project?"


print("\n==============================")
print("COMPLETE RAG TEST")
print("==============================")


print("\nQuestion:")
print(query)


result = ask_rag(
    query,
    allow_web_fallback=False
)


print("\nSTATUS:")
print(result["status"])


print("\nSOURCE:")
print(result["source"])


print("\nANSWER:")
print(result["answer"])


print("\nEVIDENCE:")


for item in result["evidence"]:

    print("\n-------------------------")

    print(
        "Document:",
        item["document"]
    )

    print(
        "Page:",
        item["page"]
    )

    print(
        "Section:",
        item["section"]
    )

    print("\nContent:")

    print(
        item["content"]
    )