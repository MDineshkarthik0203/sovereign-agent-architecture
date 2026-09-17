# Sovereign Agent Integration Guide (Local AI • SIH 2026)

This repository contains the **LangGraph-based Sovereign Agent Architecture**, fully integrated with the local **Sovereign Intelligence Services** (`inference_service` on port 8001 and `multimodal_service` on port 8002).

All LLM reasoning, code generation, vision-language analysis, and OCR run **100% locally** with zero cloud API keys (`Groq`, `OpenAI`, `Anthropic`, `Tavily`).

---

## 🏗️ Architecture Summary

```
                       SOVEREIGN AGENT ARCHITECTURE
                                     │
                             (LangGraph Agent)
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                                                         ▼
Port 8001: inference_service                               Port 8002: multimodal_service
 (FastAPI + Ollama)                                         (FastAPI + PaddleOCR/VLM)
        │                                                         │
  ┌─────┴──────────────────┐                               ┌──────┴──────────────────┐
  ▼                        ▼                               ▼                         ▼
qwen3:4b-instruct    gemma3:4b                         PaddleOCR Engine         Gemma3 Vision
(LLM & Reasoning)   (Vision-Language)                   (Document Scan)        (Visual Extraction)
```

---

## 🚀 Quickstart: Running End-to-End Locally

### Step 1: Start Ollama Server
Make sure Ollama is installed and running locally with the required models:
```bash
# Start Ollama service (Port 11434)
ollama serve

# Ensure models are downloaded
ollama pull qwen3:4b-instruct-2507-q4_K_M
ollama pull gemma3:4b
```

---

### Step 2: Start Sovereign Microservices
In your local `SIH/intelligence` directory:

```bash
# 1. Start Inference Microservice (Port 8001)
cd C:\Users\somat\Desktop\SIH\intelligence\inference_service
uvicorn main:app --port 8001 --reload

# 2. Start Multimodal OCR/VLM Microservice (Port 8002)
cd C:\Users\somat\Desktop\SIH\intelligence\multimodal_service
uvicorn main:app --port 8002 --reload
```

Verify service health:
- `curl http://localhost:8001/health`
- `curl http://localhost:8002/health`

---

### Step 3: Run the Sovereign Agent (LangGraph)
Set python environment and run your queries through `sovereign-agent-architecture`:

```python
from sovereign_agent.graph import build_graph

# Compile the sovereign agent graph
app = build_graph()

# 1. Text Query Test (routed via LocalLLM on 8001)
initial_state = {
    "question": "Explain the step-by-step pipeline for inspecting thermal power plant valves.",
    "observations": [],
    "execution_history": [],
    "tool_results": [],
    "retry_count": 0
}

result = app.invoke(initial_state)
print("FINAL ANSWER:\n", result.get("final_answer"))
```

```python
# 2. Vision / Document Scan Test (routed via Multimodal Service on 8002)
vision_state = {
    "question": "Analyze this inspection image and extract key values.",
    "file_path": "path/to/inspection_report.png",
    "observations": [],
    "execution_history": [],
    "tool_results": [],
    "retry_count": 0
}

result = app.invoke(vision_state)
print("VISION RESULT:\n", result.get("final_answer"))
```

---

## 🔒 Sovereignty & Offline Compliance
- **Zero Cloud API Calls**: All calls to `ChatGroq` / `ChatOpenAI` have been replaced by `LocalLLM` (`src/sovereign_agent/inference_client.py`).
- **No Internet Required**: The entire agent operates offline once local models and python packages are installed.
- **Microservice Decoupling**: The LangGraph agent communicates with the inference tier strictly via REST APIs (`http://localhost:8001` and `http://localhost:8002`).
