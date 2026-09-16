from langgraph.graph import StateGraph,START,END
from sovereign_agent.state import AgentState
from sovereign_agent.router import router,route_to_agent,verification_router
from sovereign_agent.nodes import coding_agent,document_agent,calculation_agent,vision_agent,general_agent,verify_agent,deliver_agent,planner_agent,replan_agent

def build_graph():
    builder=StateGraph(AgentState)
    builder.add_node("router",router)
    builder.add_node("planner_agent",planner_agent)
    builder.add_node("coding_agent",coding_agent)
    builder.add_node("document_agent",document_agent)
    builder.add_node("calculation_agent",calculation_agent)
    builder.add_node("vision_agent",vision_agent)
    builder.add_node("general_agent",general_agent)
    builder.add_node("verify_agent",verify_agent)
    builder.add_node("deliver_agent",deliver_agent)
    builder.add_node("replan_agent",replan_agent)
    builder.add_edge(START,"router")
    builder.add_edge("router","planner_agent")

    builder.add_conditional_edges("planner_agent",
    route_to_agent,
    {
            "coding_agent": "coding_agent",
            "document_agent": "document_agent",
            "calculation_agent": "calculation_agent",
            "vision_agent": "vision_agent",
            "general_agent": "general_agent",
        }
    )
    builder.add_edge("coding_agent","verify_agent")
    builder.add_edge("document_agent","verify_agent")
    builder.add_edge("calculation_agent","verify_agent")
    builder.add_edge("vision_agent","verify_agent")
    builder.add_edge("general_agent","verify_agent")

    builder.add_conditional_edges(
        "verify_agent",
        verification_router,
        {
            "deliver_agent":"deliver_agent",
            "replan_agent":"replan_agent"
        }
    )
    builder.add_conditional_edges("replan_agent",
    route_to_agent,
    {
        "coding_agent":"coding_agent",
        "document_agent":"document_agent",
        "calculation_agent":"calculation_agent",
        "vision_agent":"vision_agent",
        "general_agent":"general_agent"
    }
    )
    builder.add_edge("deliver_agent",END)

    graph=builder.compile()
    return graph
app=build_graph()


