from sovereign_agent.graph import app


result = app.invoke({

    "question": "Calculate 10 / 0",

    "route": "",

    "supervisor_reason": "",

    "plan": [],

    "current_agent": "",

    "agent_result": "",

    "tool_results": [],
    "execution_history": [],
    "document_content": "",

    "observations": [],

    "verification": "",

    "verification_status": False,

    "retry_count": 0,

    "final_answer": ""

})


print("\n==============================")
print("ROUTE")
print("==============================")
print(result["route"])


print("\n==============================")
print("PLAN")
print("==============================")

for step in result["plan"]:
    print(step)


print("\n==============================")
print("SUPERVISOR REASON")
print("==============================")
print(result["supervisor_reason"])


print("\n==============================")
print("CURRENT AGENT")
print("==============================")
print(result["current_agent"])


print("\n==============================")
print("AGENT RESULT")
print("==============================")
print(result["agent_result"])


print("\n==============================")
print("TOOL RESULTS")
print("==============================")

for tool_result in result["tool_results"]:
    print(tool_result)


print("\n==============================")
print("OBSERVATIONS")
print("==============================")

for observation in result["observations"]:
    print(observation)


print("\n==============================")
print("VERIFICATION")
print("==============================")
print(result["verification"])


print("\n==============================")
print("FINAL ANSWER")
print("==============================")
print(result["final_answer"])

print("\n==============================")
print("EXECUTION HISTORY")
print("==============================")

for history in result["execution_history"]:
    print(history)