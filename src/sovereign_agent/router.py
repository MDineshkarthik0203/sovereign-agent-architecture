from sovereign_agent.state import AgentState


def router(state: AgentState):

    question = state["question"].lower()


    # ============================================================
    # 1. CODE / CODE EXECUTION
    # ============================================================

    if any(
        phrase in question
        for phrase in [
            "write and execute",
            "write and run",
            "execute",
            "run the code",
            "run this code",
            "test the code",
            "test this program",
            "execute the code",
            "execute this program"
        ]
    ):

        return {
            "route": "coding",
            "supervisor_reason": (
                "The request is related to software development "
                "or code execution."
            ),
            "current_agent": "coding_agent"
        }


    # ============================================================
    # 2. FILE WRITING / ARTIFACT GENERATION
    # ============================================================

    if (
        any(
            phrase in question
            for phrase in [
                "write file",
                "write the file",
                "write to file",
                "write to the file",
                "save to file",
                "save the file",
                "save this file",
                "create file",
                "create a file",
                "generate file",
                "generate a file",
                "create artifact",
                "create an artifact",
                "generate artifact",
                "generate an artifact",
                "create report",
                "create a report",
                "generate report",
                "generate a report",
                "create note",
                "create a note",
                "generate note",
                "generate a note"
            ]
        )
        or (
            "write" in question
            and "file" in question
        )
        or (
            "save" in question
            and "file" in question
        )
    ):

        return {
            "route": "document",
            "supervisor_reason": (
                "The request requires writing, saving, "
                "or generating a file."
            ),
            "current_agent": "document_agent"
        }


    # ============================================================
    # 3. FILE READING
    # ============================================================

    if (
        any(
            phrase in question
            for phrase in [
                "read file",
                "read the file",
                "open file",
                "open the file",
                "read document",
                "read the document",
                "summarize file",
                "summarize the file",
                "summarize document",
                "summarize report",
                "document",
                "report",
                "knowledge base",
                "search",
                "lookup",
                "info",
                "information",
                "what is",
                "who is",
                "where is",
                "latest"
            ]
        )
        or (
            "read" in question
            and "file" in question
        )
    ):

        return {
            "route": "document",
            "supervisor_reason": (
                "The request requires reading or "
                "understanding a document."
            ),
            "current_agent": "document_agent"
        }


    # ============================================================
    # 4. CALCULATION
    # ============================================================

    if any(
        word in question
        for word in [
            "calculate",
            "calculation",
            "percentage",
            "average",
            "formula",
            "equation"
        ]
    ):

        return {
            "route": "calculation",
            "supervisor_reason": (
                "The request requires mathematical "
                "or numerical reasoning."
            ),
            "current_agent": "calculation_agent"
        }


    # ============================================================
    # 5. VISION
    # ============================================================

    if any(
        word in question
        for word in [
            "image",
            "photo",
            "scan",
            "drawing",
            "p&id",
            "pid"
        ]
    ):

        return {
            "route": "vision",
            "supervisor_reason": (
                "The request requires visual or "
                "scanned-document understanding."
            ),
            "current_agent": "vision_agent"
        }


    # ============================================================
    # 6. GENERAL
    # ============================================================

    return {
        "route": "general",
        "supervisor_reason": (
            "The request does not match a specialized "
            "task category."
        ),
        "current_agent": "general_agent"
    }


# ================================================================
# ROUTE TO SPECIALIST AGENT
# ================================================================

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


# ================================================================
# VERIFICATION ROUTER
# ================================================================

def verification_router(state: AgentState):

    if state["verification_status"]:
        return "deliver_agent"

    if state["retry_count"] >= 2:
        return "deliver_agent"

    return "replan_agent"


# ================================================================
# OBSERVATION ROUTER
# ================================================================

def observation_router(state: AgentState):

    tool_results = state["tool_results"]


    if any(
        "File Reader:" in result
        for result in tool_results
    ):

        return "document_processor"


    return "verify_agent"