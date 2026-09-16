from sovereign_agent.state import AgentState


def router(state: AgentState):

    question = state["question"].lower()

    if any(word in question for word in [
        "code",
        "python",
        "program",
        "debug",
        "function",
        "script"
    ]):
        return {
            "route": "coding",
            "supervisor_reason": "The request is related to software development.",
            "current_agent": "coding_agent"
        }

    elif any(word in question for word in [
        "document",
        "report",
        "summarize",
        "summary",
        "approval",
        "note"
    ]):
        return {
            "route": "document",
            "supervisor_reason": "The request requires document understanding or document generation.",
            "current_agent": "document_agent"
        }

    elif any(word in question for word in [
        "calculate",
        "calculation",
        "equation",
        "percentage",
        "average",
        "formula"
    ]):
        return {
            "route": "calculation",
            "supervisor_reason": "The request requires mathematical or numerical reasoning.",
            "current_agent": "calculation_agent"
        }

    elif any(word in question for word in [
        "image",
        "photo",
        "scan",
        "drawing",
        "p&id",
        "pid"
    ]):
        return {
            "route": "vision",
            "supervisor_reason": "The request requires visual or scanned-document understanding.",
            "current_agent": "vision_agent"
        }

    else:
        return {
            "route": "general",
            "supervisor_reason": "The request does not match a specialized task category.",
            "current_agent": "general_agent"
        }

def route_to_agent(state: AgentState):

    route = state["route"]

    if route == "coding":
        return "coding_agent"

    elif route == "document":
        return "document_agent"

    elif route == "calculation":
        return "calculation_agent"

    elif route == "vision":
        return "vision_agent"

    else:
        return "general_agent"

def verification_router(state:AgentState):
    if state["verification_status"]:
        return "deliver_agent"
    if state["retry_count"]>=2:
        return "deliver_agent"
    return "replan_agent"