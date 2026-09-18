import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any

from sovereign_agent.graph import app as agent_app

app = FastAPI(title="Sovereign Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRunRequest(BaseModel):
    question: str
    context: Optional[str] = ""
    web_permission_granted: Optional[bool] = False
    needs_web_permission: Optional[bool] = False


class AgentRunResponse(BaseModel):
    success: bool
    route: str
    currentAgent: str
    supervisorReason: str
    plan: List[Any]
    verification: str
    finalAnswer: str
    needsWebPermission: bool = False
    webPermissionGranted: bool = False


@app.post("/agent/run", response_model=AgentRunResponse)
def run_agent(req: AgentRunRequest):
    initial_state = {
        "question": req.question,
        "route": "",
        "supervisor_reason": "",
        "plan": [],
        "current_agent": "",
        "agent_result": "",
        "tool_results": [],
        "execution_history": [],
        "document_content": req.context or "",
        "observations": [],
        "verification": "",
        "verification_status": False,
        "retry_count": 0,
        "final_answer": "",
        "web_permission_granted": req.web_permission_granted or False,
        "needs_web_permission": req.needs_web_permission or False,
    }

    try:
        result = agent_app.invoke(initial_state)

        return AgentRunResponse(
            success=True,
            route=result.get("route", ""),
            currentAgent=result.get("current_agent", ""),
            supervisorReason=result.get("supervisor_reason", ""),
            plan=result.get("plan", []),
            verification=result.get("verification", ""),
            finalAnswer=result.get("final_answer", ""),
            needsWebPermission=result.get("needs_web_permission", False),
            webPermissionGranted=result.get("web_permission_granted", False),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("sovereign_agent.server:app", host="0.0.0.0", port=8000, reload=True)
