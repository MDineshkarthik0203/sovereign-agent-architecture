from sovereign_agent.graph import app


initial_state = {
    "question": "What is the purpose of the project?",

    "route": "",

    "supervisor_reason": "",

    "plan": [],

    "current_agent": "",

    "agent_result": "",

    "execution_history": [],

    "tool_results": [],

    "document_content": "",

    "observations": [],

    "verification": "",

    "verification_status": False,

    "retry_count": 0,

    "final_answer": ""
}


result = app.invoke(
    initial_state
)


print("\n==============================")
print("LANGGRAPH + RAG TEST")
print("==============================")


print("\nROUTE:")
print(result["route"])


print("\nCURRENT AGENT:")
print(result["current_agent"])


print("\nPLAN:")
for step in result["plan"]:
    print(step)


print("\nAGENT RESULT:")
print(result["agent_result"])


print("\nVERIFICATION:")
print(result["verification"])


print("\nFINAL ANSWER:")
print(result["final_answer"])


print("\nEXECUTION HISTORY:")

for item in result["execution_history"]:
    print("-", item)