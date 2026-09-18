import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sovereign_agent.graph import app


initial_state = {
    "question": "Write the generated content to a file named project_summary.txt",
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


print("==============================")
print("LANGGRAPH + SANDBOX WRITE TEST")
print("==============================")


result = app.invoke(initial_state)


print("\nROUTE:")
print(result["route"])


print("\nCURRENT AGENT:")
print(result["current_agent"])


print("\nPLAN:")
for step in result["plan"]:
    print(step)


print("\nAGENT RESULT:")
print(result["agent_result"])


print("\nTOOL RESULTS:")
for item in result["tool_results"]:
    print(item)


print("\nOBSERVATIONS:")
for item in result["observations"]:
    print("-", item)


print("\nVERIFICATION:")
print(result["verification"])


print("\nFINAL ANSWER:")
print(result["final_answer"])


print("\nEXECUTION HISTORY:")
for item in result["execution_history"]:
    print("-", item)