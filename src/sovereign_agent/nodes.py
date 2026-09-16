from urllib3 import response
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sovereign_agent.state import AgentState
load_dotenv()
def get_llm():
    llm=ChatGroq(model="openai/gpt-oss-20b",temperature=0)
    return llm

def planner_agent(state:AgentState):
    llm=get_llm()
    question=state["question"]
    selected_agent=state["current_agent"]
    prompt = f"""
You are the Planner Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Selected agent:
{selected_agent}

Create a simple execution plan for solving the user's request.

Return only a numbered list of steps.

Example:

1. Understand the request
2. Perform the required operation
3. Check the result
4. Prepare the final response
"""
    response=llm.invoke(prompt)
    plan_text = response.content

    plan = [
        line.strip()
        for line in plan_text.split("\n")
        if line.strip()
    ]
    return{
        "plan":plan,
        "observations":["Planner Created an execution plan"]
    }
def coding_agent(state:AgentState):
    question=state["question"]
    llm=get_llm()
    prompt = f"""
You are the Coding Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Solve the coding task.

Provide:
1. Explanation
2. Code
3. Important notes
"""
    response=llm.invoke(prompt)
    content=response.content
    return {
        "agent_result":content,
        "observation":["Coding Agent completed the requested coding task"]
    }

def document_agent(state:AgentState):
    llm=get_llm()
    question=state["question"]
    prompt = f"""
You are the Document Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Handle the document-related task.

Provide a clear and structured response.
"""
    response=llm.invoke(prompt)
    content=response.content
    return{
        "agent_result":content,
        "observations":["Document Agent Completed document task"]
    }

def calculation_agent(state:AgentState):
    llm=get_llm()
    question=state["question"]
    prompt = f"""
You are the Calculation Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Perform the required calculation carefully.

Show:
1. Formula
2. Calculation steps
3. Final answer
"""
    response=llm.invoke(prompt)
    content=response.content
    return{
        "agent_result":content,
        "observations":["Calculation Agent Completed calculation task"]
    }

def vision_agent(state:AgentState):
    question=state["question"]
    llm=get_llm()
    prompt = f"""
You are the Vision Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

The system may later provide images or scanned documents.

For this prototype, explain how the visual task should be handled.
"""
    response=llm.invoke(prompt)
    content=response.content
    return{
        "agent_result":content,
        "observations":["Vision Agent processed the visual-task request"]
    }
def general_agent(state:AgentState):
    llm=get_llm()
    question=state["question"]
    prompt = f"""
You are the General Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Answer the user's request clearly and accurately.
"""
    response=llm.invoke(prompt)
    content=response.content
    return{
        "agent_result":content,
        "observations":["General Agent completed the request"]
    }

def verify_agent(state:AgentState):
    question=state["question"]
    agent_result=state["agent_result"]
    llm=get_llm()

    prompt = f"""
You are the Verification Agent.

User request:
{question}

Agent result:
{agent_result}

Check whether the result correctly addresses the user's request.

Return exactly:

STATUS: PASS
or
STATUS: FAIL

Then give a short reason.
"""
    response=llm.invoke(prompt)
    verification=response.content
    status=verification.upper().startswith("STATUS: PASS")
    return{
        "verification":verification,
        "verification_status":status
    }

def replan_agent(state:AgentState):
    llm=get_llm()
    question=state["question"]
    previous_plan=state["plan"]
    previous_agent_result=state["agent_result"]
    previous_verification=state["verification"]
    prompt = f"""
You are the Replanning Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Previous plan:
{previous_plan}

Previous agent result:
{previous_agent_result}

Verification result:
{previous_verification}

Create a corrected plan to solve the request.

Focus on fixing the problem identified by verification.

Return only a numbered list of steps.
"""
    response=llm.invoke(prompt)
    plan_text = response.content

    plan = [
        line.strip()
        for line in plan_text.split("\n")
        if line.strip()
    ]
    return{
        "plan":plan,
        "retry_count":state["retry_count"],
        "observations":["Verification is failed ,New plan is created"]
    }

def deliver_agent(state:AgentState):
    return{
        "final_answer":state["agent_result"]
    }