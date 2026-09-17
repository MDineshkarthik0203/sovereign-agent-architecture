# Progress Report — Intelligence Service (M2) & Multimodal Engine (M4)

**Project**: SIH 2026 — Sovereign On-Premise Agentic AI Workbench  
**Role**: LLM/Inference Engineer (M2) + Multimodal AI Engineer (M4)  
**Status**: All services working, integrated, structured under `intelligence/`, and verified end-to-end.

---

## 1. Executive Summary & Setup Fixes

- **PaddleOCR Setup Issue Fixed**:
  - **Diagnostic**: System default `python` is 3.14.6, which fails to find pre-built wheels for `paddlepaddle==2.6.2`.
  - **Resolution**: Workspace virtual environment `venv` uses **Python 3.11.9**, where `paddlepaddle==2.6.2` and `paddleocr==2.9.1` are fully compatible and installed.
  - **Fix**: Run all commands via `.\venv\Scripts\python.exe` / `.\venv\Scripts\uvicorn.exe`.
  - Added missing dependency `python-multipart` required by FastAPI for multipart form file uploads (`UploadFile`).

- **Services Status**:
  - `intelligence/inference_service` running on **port 8001** (FastAPI wrapping local Ollama server).
  - `intelligence/multimodal_service` running on **port 8002** (PaddleOCR + HTTP calls to `inference_service` + Chat-First UI Dashboard).
  - End-to-end vision-language pipeline verified: uploaded scanned document -> PaddleOCR text/lines -> structured JSON output via local Ollama models.

---

## 2. API Contracts & Architecture

### A. Inference Service (`intelligence/inference_service/main.py` — Port 8001)
- **Endpoint**: `POST /generate`
- **Registered Models**:
  - `"qwen3:4b-instruct-2507-q4_K_M"` (Reasoning/Fast instruct, `think=False` for ~5-15s CPU response)
  - `"qwen3:4b"` (Reasoning fallback)
  - `"gemma3:4b"` (Vision-Language model)
- **Standard Request Contract (Without Context)**:
  ```json
  {
    "model_id": "qwen3:4b-instruct-2507-q4_K_M",
    "messages": [{"role": "user", "content": "Extract data..."}],
    "config": {"temperature": 0.2, "max_tokens": 1024}
  }
  ```
- **Standard Response Contract**:
  ```json
  {
    "model_id": "qwen3:4b-instruct-2507-q4_K_M",
    "response": "Cleaned response string without <think> tags",
    "usage": {"prompt_tokens": 45, "completion_tokens": 120, "latency_ms": 12500}
  }
  ```

---

## 3. RAG-Ready Intelligence Extension (Teammate Integration Interface)

> [!NOTE]
> **Team Boundary Note**:
> Vector database storage, PDF ingestion, chunking, embeddings, and retrieval are handled by the **Local RAG Teammate**. Web search, internet retrieval, and user permissions are handled by the **External Retrieval Teammate**.
> The **Intelligence Service (this module)** has **ZERO internet dependency** and communicates solely with local Ollama models (`http://localhost:11434`) on the air-gapped machine.

### RAG-Grounded Request Contract (Optional `context`)
To provide retrieved context from the Local RAG service, the Agent or RAG teammate passes the optional `context` object in `POST /generate`:

```json
{
  "model_id": "qwen3:4b-instruct-2507-q4_K_M",
  "messages": [
    {"role": "user", "content": "What is the recommended cooling system pressure?"}
  ],
  "context": {
    "source": "local_rag",
    "documents": [
      {
        "document": "Sovereign_Node_Specs.pdf",
        "page": 24,
        "content": "Cooling System Specification: Operating pressure for Node A is strictly 101.3 kPa."
      }
    ]
  }
}
```

### RAG Response Contract with Source Attribution (`sources`)
When `context` is provided, `inference_service` grounds the LLM prompt using strict instruction/content separation to prevent prompt injection, and returns document page attributions in `sources`:

```json
{
  "model_id": "qwen3:4b-instruct-2507-q4_K_M",
  "response": "Based on the retrieved specification document, the recommended cooling system pressure for Air-Gapped Workbench Node A is 101.3 kPa.",
  "usage": {
    "prompt_tokens": 142,
    "completion_tokens": 32,
    "latency_ms": 14850
  },
  "sources": [
    {
      "document": "Sovereign_Node_Specs.pdf",
      "page": 24
    }
  ]
}
```

---

## 4. Multimodal Service (`intelligence/multimodal_service/main.py` — Port 8002)
- **Endpoint**: `POST /analyze?mode=fast` (or `mode=vlm`)
- **Processing Modes**:
  - `mode=fast` (**Recommended for Live Demo on CPU**): Runs offline PaddleOCR to extract text lines + confidence, then calls `qwen3:4b-instruct` to extract clean structured JSON in **~5-15 seconds**.
  - `mode=vlm`: Encodes image in Base64 and calls `gemma3:4b` direct vision model (**~30-60 seconds** on CPU). Automatically falls back to fast mode if VLM times out.
- **Request Contract**: Multipart form data with key `file` (image `.png`, `.jpg`, `.pdf` frame).
- **Response Contract**:
  ```json
  {
    "page_ref": "file://test_report.png",
    "ocr_text": "EQUIPMENT INSPECTION REPORT\nReport ID: INSP-2026-9941\n...",
    "ocr_lines": [{"text": "EQUIPMENT INSPECTION REPORT", "confidence": 0.998, "bbox": [...]}],
    "ocr_avg_confidence": 0.985,
    "structured_fields": {
      "document_type": "EQUIPMENT INSPECTION REPORT",
      "report_id": "INSP-2026-9941",
      "inspector": "M4 Engineer",
      "status": "OPERATIONAL"
    },
    "vlm_raw_response": "```json\n{...}\n```",
    "execution_time_ms": 11200,
    "mode_used": "fast"
  }
  ```

---

## 5. CPU Latency Optimization & Demo Recommendations

> [!TIP]
> **Live Demo Strategy (2-Day Deadline, CPU Only)**:
> 1. Use `mode=fast` (`POST http://localhost:8002/analyze?mode=fast`) for live presentations. OCR text extraction + text LLM JSON structuring is fast (~10s) and predictable on CPU.
> 2. `qwen3:4b-instruct-2507-q4_K_M` has `think=False` enabled in `inference_service` to bypass latency-heavy reasoning chains.
> 3. Highlight full offline sovereignty: disconnect internet during demo — both PaddleOCR and Ollama models operate 100% locally.

---

## 6. How to Run & Demo

### Terminal 1: Start Inference Service (Port 8001)
```powershell
cd c:\Users\somat\Desktop\SIH\intelligence\inference_service
..\..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001
```

### Terminal 2: Start Multimodal Service (Port 8002)
```powershell
cd c:\Users\somat\Desktop\SIH\intelligence\multimodal_service
..\..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8002
```

### Terminal 3: Run Full RAG & Multimodal Pipeline Verification
```powershell
cd c:\Users\somat\Desktop\SIH
.\venv\Scripts\python.exe intelligence/sample_data/verify_rag_extension.py
```
