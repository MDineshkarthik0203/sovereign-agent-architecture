from sovereign_agent.rag.rag_implementation.generator import (
    generate_answer
)


evidence = [
    {
        "document": "sample.pdf",
        "page": 1,
        "section": "Unknown",
        "content": (
            "Sovereign Agentic AI Workbench\n"
            "Project Type: AI Agent System\n"
            "Status: Development\n"
            "Purpose: Confidential industrial "
            "document processing."
        )
    }
]


query = "What is the purpose of the project?"


answer = generate_answer(
    query,
    evidence
)


print("\n==============================")
print("OPENAI GENERATION TEST")
print("==============================")

print("\nQuestion:")
print(query)

print("\nAnswer:")
print(answer)