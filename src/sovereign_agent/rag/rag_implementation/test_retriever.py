from sovereign_agent.rag.rag_implementation.retriever import retrieve_documents


query = "What is this document about?"


result = retrieve_documents(query)


print("\n==============================")
print("RAG RETRIEVAL TEST")
print("==============================")


print("\nSTATUS:")
print(result["status"])


print("\nEVIDENCE:")


for item in result["evidence"]:

    print("\n-------------------------")

    print("Document:", item["document"])

    print("Page:", item["page"])

    print("Section:", item["section"])

    print("\nContent:")

    print(item["content"])

    print("\nSource:", item["source_type"])