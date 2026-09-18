import os
import httpx
from dotenv import load_dotenv

from sovereign_agent.inference_client import LocalLLM
from sovereign_agent.state import AgentState
from sovereign_agent.rag.rag_implementation.rag import ask_rag

load_dotenv()


# ============================================================
# LLM
# ============================================================

def get_llm():
    return LocalLLM()


# ============================================================
# PLANNER AGENT
# ============================================================

def planner_agent(state: AgentState):

    llm = get_llm()

    question = state["question"]
    selected_agent = state["current_agent"]

    prompt = f"""
You are the Planner Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Selected agent:
{selected_agent}

Create a simple execution plan for solving the user's request.

Return only a numbered list of steps.
"""

    response = llm.invoke(prompt)

    plan_text = response.content

    plan = [
        line.strip()
        for line in plan_text.split("\n")
        if line.strip()
    ]

    return {
        "plan": plan,
        "observations": state["observations"] + [
            "Planner Agent created an execution plan."
        ],
        "execution_history": state["execution_history"] + [
            "Planner Agent created an execution plan"
        ]
    }


# ============================================================
# CODING AGENT
# ============================================================

def coding_agent(state: AgentState):

    question = state["question"]

    llm = get_llm()

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

    response = llm.invoke(prompt)

    content = response.content

    return {
        "agent_result": content,

        "observations": state["observations"] + [
            "Coding Agent completed the requested coding task."
        ],

        "execution_history": state["execution_history"] + [
            "Coding Agent executed the coding task."
        ]
    }


# ============================================================
# DOCUMENT AGENT + RAG
# ============================================================

def document_agent(state: AgentState):

    question = state["question"]
    question_lower = question.lower()

    tool_results = state["tool_results"].copy()
    observations = state["observations"].copy()


    # ============================================================
    # FILE GENERATION
    # ============================================================

    is_file_generation = (
        (
            "write" in question_lower
            and "file" in question_lower
        )
        or
        (
            "save" in question_lower
            and "file" in question_lower
        )
        or
        (
            "create" in question_lower
            and "file" in question_lower
        )
        or
        (
            "generate" in question_lower
            and "file" in question_lower
        )
    )


    if is_file_generation:

        llm = get_llm()

        prompt = f"""
You are the Document Generation Agent
inside a Sovereign Agentic AI Workbench.

The user wants to generate content and write it
to a file.

USER REQUEST:
{question}

Your task is to generate the actual content
that should be written to the requested file.

IMPORTANT RULES:

1. Generate useful, complete content.
2. Do NOT say that information is unavailable.
3. Do NOT say that no content was provided.
4. Do NOT refuse the task.
5. Do NOT return instructions explaining how to
   create the file.
6. Return the actual content that should be written.
7. If the user did not provide project-specific
   information, create a clearly marked generic
   project-summary template.
8. Do not use RAG for this task.
9. Do not wrap the entire response in code fences.
10. The returned content will be passed directly
    to the Sandbox file-writing tool.

Return ONLY the file content.

Generate the content now.
"""

        response = llm.invoke(prompt)

        content = response.content.strip()


        # Safety check
        if not content:

            raise ValueError(
                "Document Agent generated empty file content."
            )


        observations.append(
            "Document Agent generated content for file creation."
        )

        return {
            "agent_result": content,

            "tool_results": tool_results,

            "observations": observations,

            "execution_history": state["execution_history"] + [
                "Document Agent generated file content."
            ]
        }


    # ============================================================
    # NORMAL DOCUMENT QUESTION → RAG
    # ============================================================

    result = ask_rag(
        question,
        allow_web_fallback=True
    )


    if result["source"] == "local":

        content = result["answer"]

        evidence = result.get(
            "evidence",
            []
        )

        tool_results.append(
            "RAG Status: SUCCESS"
        )

        tool_results.append(
            f"RAG Evidence: {evidence}"
        )

        observations.append(
            "Document Agent used the local RAG knowledge base."
        )


    elif result["source"] == "web":

        web_results = result.get(
            "web_results",
            []
        )

        web_context = "\n\n".join(
            [
                f"Title: {item.get('title', '')}\n"
                f"URL: {item.get('url', '')}\n"
                f"Content: {item.get('content', '')}"
                for item in web_results
            ]
        )

        content = (
            "The requested information was not found "
            "in the local knowledge base.\n\n"
            "External web evidence:\n\n"
            f"{web_context}"
        )

        tool_results.append(
            "RAG Status: LOCAL KNOWLEDGE NOT FOUND"
        )

        tool_results.append(
            f"Web Evidence: {web_results}"
        )

        observations.append(
            "Document Agent used web search."
        )


    else:

        content = result["answer"]

        tool_results.append(
            "RAG Status: NO EVIDENCE FOUND"
        )

        observations.append(
            "Document Agent could not find sufficient information."
        )


    return {
        "agent_result": content,

        "tool_results": tool_results,

        "observations": observations,

        "execution_history": state["execution_history"] + [
            "Document Agent executed the RAG workflow."
        ]
    }

def document_processor(state: AgentState):

    llm = get_llm()

    question = state["question"]
    document_content = state["document_content"]

    prompt = f"""
You are the Document Processing Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Document content:
{document_content}

Use the document content as the primary source.

Rules:
- Do not invent information.
- Answer only using information present in the document.
- If the requested information is not present, explicitly say so.
- Give a clear and structured answer.

Return the final answer for the user.
"""

    response = llm.invoke(prompt)

    return {
        "agent_result": response.content,

        "observations": state["observations"] + [
            "Document Processor analyzed the file content."
        ],

        "execution_history": state["execution_history"] + [
            "Document Processor analyzed the document content."
        ]
    }


# ============================================================
# CALCULATION AGENT
# ============================================================

def calculation_agent(state: AgentState):

    llm = get_llm()

    question = state["question"]

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

    response = llm.invoke(prompt)

    return {

        "agent_result": response.content,

        "observations": state["observations"] + [
            "Calculation Agent completed the calculation task."
        ],

        "execution_history": state["execution_history"] + [
            "Calculation Agent executed the calculation task."
        ]
    }


# ============================================================
# VISION AGENT
# ============================================================

def vision_agent(state: AgentState):

    question = state["question"]
    file_path = state.get("file_path") or state.get("image_path")

    if file_path and os.path.exists(file_path):
        try:
            multimodal_url = os.getenv("MULTIMODAL_SERVICE_URL", "http://172.16.216.12:8002/analyze?mode=fast")
            with open(file_path, "rb") as f:
                response = httpx.post(
                    multimodal_url,
                    files={"file": (os.path.basename(file_path), f)},
                    timeout=300
                )
            response.raise_for_status()
            data = response.json()

            ocr_text = data.get("ocr_text", "")
            confidence = data.get("confidence", 0)
            fields = data.get("structured_fields", {})
            fields_str = "\n".join([f"- {k}: {v}" for k, v in fields.items()]) if fields else "None"

            content = (
                f"### Multimodal Document Analysis Result\n"
                f"**File**: {os.path.basename(file_path)}\n"
                f"**OCR Confidence**: {confidence}%\n\n"
                f"**Extracted Key Fields**:\n{fields_str}\n\n"
                f"**Extracted Text / OCR Summary**:\n{ocr_text[:1500]}"
            )

            return {
                "agent_result": content,
                "observations": state["observations"] + [
                    f"Vision Agent processed image/document {os.path.basename(file_path)} via local Multimodal Service (OCR confidence: {confidence}%)."
                ],
                "execution_history": state["execution_history"] + [
                    "Vision Agent executed local OCR & visual analysis workflow."
                ]
            }
        except Exception as e:
            content = f"Error during local visual processing: {str(e)}"

    llm = get_llm()

    prompt = f"""
You are the Vision Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Provide a detailed response for handling this visual request using the local Gemma3/Qwen3 vision pipeline.
"""

    response = llm.invoke(prompt)

    return {

        "agent_result": response.content,

        "observations": state["observations"] + [
            "Vision Agent completed the visual task."
        ],

        "execution_history": state["execution_history"] + [
            "Vision Agent executed the visual task."
        ]
    }


# ============================================================
# GENERAL AGENT
# ============================================================

def general_agent(state: AgentState):

    llm = get_llm()

    question = state["question"]

    prompt = f"""
You are the General Agent in a Sovereign Agentic AI Workbench.

User request:
{question}

Answer the user's request clearly and accurately.
"""

    response = llm.invoke(prompt)

    return {

        "agent_result": response.content,

        "observations": state["observations"] + [
            "General Agent completed the general task."
        ],

        "execution_history": state["execution_history"] + [
            "General Agent executed the general task."
        ]
    }


# ============================================================
# VERIFY AGENT
# ============================================================

def verify_agent(state: AgentState):

    question = state["question"]

    agent_result = state["agent_result"]

    tool_results = state["tool_results"]


    # ============================================================
    # 1. HARD FAILURE CHECKS
    # ============================================================

    for result in tool_results:

        if (
            "Success: False" in result
            or
            "Calculation error:" in result
            or
            "Execution timed out" in result
            or
            "Artifact creation failed:" in result
            or
            "File not found:" in result
            or
            "Error reading" in result
            or
            "RAG Status: NO EVIDENCE FOUND" in result
            or
            "File Content Verification: FAIL" in result
        ):

            return {
                "verification": (
                    "STATUS: FAIL\n"
                    "Reason: Required tool execution or "
                    "content verification failed."
                ),

                "verification_status": False,

                "execution_history": state["execution_history"] + [
                    "Verification Agent detected a tool or evidence failure."
                ]
            }


    # ============================================================
    # 2. DETERMINISTIC FILE VERIFICATION
    # ============================================================

    if "File Content Verification: PASS" in tool_results:

        return {
            "verification": (
                "STATUS: PASS\n"
                "Reason: The Sandbox successfully wrote the file, "
                "read it back, and confirmed that the written content "
                "matches the generated content."
            ),

            "verification_status": True,

            "execution_history": state["execution_history"] + [
                "Verification Agent confirmed file content using Sandbox read-back verification."
            ]
        }


    # ============================================================
    # 3. CODE EXECUTION VERIFICATION
    # ============================================================

    if any(
        "Sandbox Executor:" in result
        for result in tool_results
    ):

        sandbox_evidence = "\n".join(tool_results)

        if (
            "Status: success" in sandbox_evidence
            and
            "Exit Code: 0" in sandbox_evidence
        ):

            return {
                "verification": (
                    "STATUS: PASS\n"
                    "Reason: Python code executed successfully "
                    "inside the Sandbox."
                ),

                "verification_status": True,

                "execution_history": state["execution_history"] + [
                    "Verification Agent confirmed successful Sandbox execution."
                ]
            }


    # ============================================================
    # 4. LLM-BASED VERIFICATION FOR OTHER TASKS
    # ============================================================

    evidence_context = "\n\n".join(
        tool_results
    )

    llm = get_llm()

    prompt = f"""
You are the Verification Agent in a
Sovereign Agentic AI Workbench.

Verify whether the final answer is supported
by the evidence produced during execution.

USER REQUEST:
{question}

AGENT RESULT:
{agent_result}

EXECUTION EVIDENCE:
{evidence_context}

RULES:

1. Compare the agent result with the evidence.
2. Do not invent evidence.
3. If the evidence supports the result, return PASS.
4. If the evidence contradicts the result, return FAIL.
5. If required evidence is missing, return FAIL.

Return exactly:

STATUS: PASS

or

STATUS: FAIL

Then provide one short reason.
"""

    response = llm.invoke(prompt)

    verification = response.content.strip()

    status = verification.upper().startswith(
        "STATUS: PASS"
    )

    return {
        "verification": verification,

        "verification_status": status,

        "execution_history": state["execution_history"] + [
            (
                "Verification Agent completed verification: "
                f"{'PASS' if status else 'FAIL'}."
            )
        ]
    }

# ============================================================
# REPLAN AGENT
# ============================================================

def replan_agent(state: AgentState):

    llm = get_llm()

    question = state["question"]

    previous_plan = state["plan"]

    previous_agent_result = state["agent_result"]

    previous_verification = state["verification"]

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

    response = llm.invoke(prompt)

    plan_text = response.content

    plan = [
        line.strip()
        for line in plan_text.split("\n")
        if line.strip()
    ]

    return {

        "plan": plan,

        "retry_count": state["retry_count"] + 1,

        "observations": state["observations"] + [
            "Verification failed. New plan was created."
        ],

        "execution_history": state["execution_history"] + [
            "Replanning Agent created a new plan after verification failure."
        ]
    }


# ============================================================
# OBSERVE AGENT
# ============================================================

def observe_agent(state: AgentState):

    tool_results = state["tool_results"]

    if tool_results:

        observation = (
            "Tool/RAG execution completed. "
            f"Results observed: {tool_results}"
        )

    else:

        observation = "No tool results were produced."

    return {

        "observations": state["observations"] + [
            observation
        ],

        "execution_history": state["execution_history"] + [
            "Observe Agent inspected the execution results."
        ]
    }


# ============================================================
# DELIVER AGENT
# ============================================================

def deliver_agent(state: AgentState):

    if not state["verification_status"]:

        final_answer = (
            "The task could not be completed successfully "
            "after multiple attempts.\n\n"
            f"Verification result:\n"
            f"{state['verification']}"
        )

    else:

        final_answer = state["agent_result"]

    return {

        "final_answer": final_answer,

        "execution_history": state["execution_history"] + [
            "Deliver Agent prepared the final response."
        ]
    }