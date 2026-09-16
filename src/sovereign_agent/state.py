from typing import TypedDict

class AgentState(TypedDict):
    question:str
    # Supervisor decision
    route:str
    supervisor_reason:str
    plan:list[str]
    current_agent:str
    agent_result:str
    tool_results:list[str]
    observations:list[str]

    verification:str
    verification_status:bool
    retry_count:int
    final_answer:str
    
