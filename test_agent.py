import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sovereign_agent.graph import app


def run_scenario(name, initial_state):
    print("\n" + "=" * 60)
    print(f" SCENARIO: {name}")
    print("=" * 60)
    
    result = app.invoke(initial_state)

    print("\nQUESTION:", result["question"])
    print("ROUTE:", result.get("route"))
    print("CURRENT AGENT:", result.get("current_agent"))
    print("NEEDS WEB PERMISSION:", result.get("needs_web_permission"))
    print("WEB PERMISSION GRANTED:", result.get("web_permission_granted"))
    print("\nFINAL ANSWER:")
    print(result.get("final_answer"))
    
    print("\nOBSERVATIONS:")
    for obs in result.get("observations", []):
        print(f" - {obs}")
        
    print("\nEXECUTION HISTORY:")
    for history in result.get("execution_history", []):
        print(f" - {history}")
        
    return result


if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "all"

    if scenario in ("1", "local", "all"):
        # Scenario 1: Local Knowledge Hit
        state_local = {
            "question": "Summarize the crude distillation unit inspection report",
            "route": "",
            "supervisor_reason": "",
            "plan": [],
            "current_agent": "",
            "agent_result": "",
            "tool_results": [],
            "execution_history": [],
            "document_content": "Crude Distillation Unit Inspection Report: Inspection performed on Unit 4 revealed mild surface corrosion on bypass valve V-104. Safety parameters within limits.",
            "observations": [],
            "file_path": "",
            "image_path": "",
            "web_permission_granted": False,
            "needs_web_permission": False,
            "verification": "",
            "verification_status": False,
            "retry_count": 0,
            "final_answer": ""
        }
        run_scenario("1. Local Document Hit", state_local)

    if scenario in ("2", "denied", "all"):
        # Scenario 2: Missing Knowledge + Permission Denied
        state_turn1 = {
            "question": "What are the latest 2026 Space Exploration milestones?",
            "route": "",
            "supervisor_reason": "",
            "plan": [],
            "current_agent": "",
            "agent_result": "",
            "tool_results": [],
            "execution_history": [],
            "document_content": "",
            "observations": [],
            "file_path": "",
            "image_path": "",
            "web_permission_granted": False,
            "needs_web_permission": False,
            "verification": "",
            "verification_status": False,
            "retry_count": 0,
            "final_answer": ""
        }
        res_turn1 = run_scenario("2a. Missing Knowledge (Initial Request -> Prompt User)", state_turn1)

        # Turn 2: User explicitly denies permission (web_permission_granted = False)
        state_turn2_denied = {
            **res_turn1,
            "web_permission_granted": False
        }
        run_scenario("2b. Missing Knowledge (User Denies Web Permission)", state_turn2_denied)

    if scenario in ("3", "granted", "all"):
        # Scenario 3: Missing Knowledge + Permission Granted
        state_turn1 = {
            "question": "What is Python programming language?",
            "route": "",
            "supervisor_reason": "",
            "plan": [],
            "current_agent": "",
            "agent_result": "",
            "tool_results": [],
            "execution_history": [],
            "document_content": "",
            "observations": [],
            "file_path": "",
            "image_path": "",
            "web_permission_granted": False,
            "needs_web_permission": False,
            "verification": "",
            "verification_status": False,
            "retry_count": 0,
            "final_answer": ""
        }
        res_turn1 = run_scenario("3a. Missing Knowledge (Initial Request -> Prompt User)", state_turn1)

        # Turn 2: User grants permission (web_permission_granted = True)
        state_turn2_granted = {
            **res_turn1,
            "web_permission_granted": True
        }
        run_scenario("3b. Missing Knowledge (User Grants Web Permission -> Web Search)", state_turn2_granted)