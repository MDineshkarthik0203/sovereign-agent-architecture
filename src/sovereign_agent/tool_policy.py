from sovereign_agent.state import AgentState


def tool_policy(state: AgentState):

    question = state["question"].lower()


    # ============================================================
    # 1. CODE EXECUTION → SANDBOX
    # ============================================================

    if any(
        phrase in question
        for phrase in [
            "execute",
            "run the code",
            "run this code",
            "test the code",
            "test this program",
            "execute the code",
            "execute this program"
        ]
    ):

        return "use_tool"


    # ============================================================
    # 2. FILE WRITING → SANDBOX
    # ============================================================

    if (
        (
            "write" in question
            and "file" in question
        )
        or
        (
            "save" in question
            and "file" in question
        )
        or
        (
            "create" in question
            and "file" in question
        )
    ):

        return "use_tool"


    # ============================================================
    # 3. FILE READING → SANDBOX
    # ============================================================

    if (
        (
            "read" in question
            and "file" in question
        )
        or
        (
            "open" in question
            and "file" in question
        )
        or
        (
            "read" in question
            and "document" in question
        )
    ):

        return "use_tool"


    # ============================================================
    # 4. ARTIFACT GENERATION → SANDBOX
    # ============================================================

    if (
        "artifact" in question
        or
        (
            "generate" in question
            and "report" in question
        )
        or
        (
            "create" in question
            and "report" in question
        )
        or
        (
            "generate" in question
            and "note" in question
        )
        or
        (
            "create" in question
            and "note" in question
        )
    ):

        return "use_tool"


    # ============================================================
    # 5. CALCULATION → CALCULATOR
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

        return "use_tool"


    # ============================================================
    # 6. DOCUMENT AGENT → RAG
    # ============================================================

    # Normal document questions are handled
    # internally by the Document Agent using RAG.

    if state.get("current_agent") == "document_agent":

        return "no_tool"


    # ============================================================
    # 7. DEFAULT
    # ============================================================

    return "no_tool"