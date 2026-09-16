from sovereign_agent.graph import app


result = app.invoke({
    "question": "Write a Python function to check whether a number is prime.",
    "route": "",
    "supervisor_reason": "",
    "plan": [],
    "current_agent": "",
    "agent_result": "",
    "tool_results": [],
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
print("VERIFICATION")
print("==============================")
print(result["verification"])

print("\n==============================")
print("FINAL ANSWER")
print("==============================")
print(result["final_answer"])
