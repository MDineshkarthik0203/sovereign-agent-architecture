from langgraph.graph import (
    StateGraph,
    START,
    END
)

from sovereign_agent.state import AgentState

from sovereign_agent.router import (
    router,
    route_to_agent,
    verification_router,
    observation_router
)

from sovereign_agent.nodes import (
    coding_agent,
    document_agent,
    document_processor,
    calculation_agent,
    vision_agent,
    general_agent,
    verify_agent,
    deliver_agent,
    planner_agent,
    replan_agent,
    observe_agent
)

from sovereign_agent.tool_policy import tool_policy

from sovereign_agent.tools.tool_executor import (
    tool_executor
)


def build_graph():

    builder = StateGraph(
        AgentState
    )


    # =========================
    # NODES
    # =========================

    builder.add_node(
        "router",
        router
    )

    builder.add_node(
        "planner_agent",
        planner_agent
    )

    builder.add_node(
        "coding_agent",
        coding_agent
    )

    builder.add_node(
        "document_agent",
        document_agent
    )

    builder.add_node(
        "document_processor",
        document_processor
    )

    builder.add_node(
        "calculation_agent",
        calculation_agent
    )

    builder.add_node(
        "vision_agent",
        vision_agent
    )

    builder.add_node(
        "general_agent",
        general_agent
    )

    builder.add_node(
        "verify_agent",
        verify_agent
    )

    builder.add_node(
        "deliver_agent",
        deliver_agent
    )

    builder.add_node(
        "replan_agent",
        replan_agent
    )

    builder.add_node(
        "tool_executor",
        tool_executor
    )

    builder.add_node(
        "observe_agent",
        observe_agent
    )


    # =========================
    # START
    # =========================

    builder.add_edge(
        START,
        "router"
    )


    # =========================
    # ROUTER → PLANNER
    # =========================

    builder.add_edge(
        "router",
        "planner_agent"
    )


    # =========================
    # PLANNER → AGENT
    # =========================

    builder.add_conditional_edges(
        "planner_agent",
        route_to_agent,
        {
            "coding_agent": "coding_agent",
            "document_agent": "document_agent",
            "calculation_agent": "calculation_agent",
            "vision_agent": "vision_agent",
            "general_agent": "general_agent"
        }
    )


    # =========================
    # AGENTS → TOOL / OBSERVE
    # =========================

    for agent in [
        "coding_agent",
        "document_agent",
        "calculation_agent",
        "vision_agent",
        "general_agent"
    ]:

        builder.add_conditional_edges(
            agent,
            tool_policy,
            {
                "use_tool": "tool_executor",
                "no_tool": "observe_agent"
            }
        )


    # =========================
    # TOOL → OBSERVE
    # =========================

    builder.add_edge(
        "tool_executor",
        "observe_agent"
    )


    # =========================
    # OBSERVE
    # =========================

    builder.add_conditional_edges(
        "observe_agent",
        observation_router,
        {
            "document_processor":
                "document_processor",

            "verify_agent":
                "verify_agent"
        }
    )


    # =========================
    # DOCUMENT PROCESSOR
    # =========================

    builder.add_edge(
        "document_processor",
        "verify_agent"
    )


    # =========================
    # VERIFICATION
    # =========================

    builder.add_conditional_edges(
        "verify_agent",
        verification_router,
        {
            "deliver_agent":
                "deliver_agent",

            "replan_agent":
                "replan_agent"
        }
    )


    # =========================
    # REPLAN
    # =========================

    builder.add_conditional_edges(
        "replan_agent",
        route_to_agent,
        {
            "coding_agent": "coding_agent",
            "document_agent": "document_agent",
            "calculation_agent": "calculation_agent",
            "vision_agent": "vision_agent",
            "general_agent": "general_agent"
        }
    )


    # =========================
    # END
    # =========================

    builder.add_edge(
        "deliver_agent",
        END
    )


    return builder.compile()


app = build_graph()