"""
Multimodal Service — owned by M4 (Multimodal AI Engineer)

Contract (Interface M4 -> Agent/M1):
    file -> {page_ref, ocr_text, ocr_lines, ocr_avg_confidence, structured_fields, vlm_raw_response}

Pipeline:
    1. Receive uploaded scanned image / document
    2. Run PaddleOCR to get high-accuracy offline OCR text and line-level confidence
    3. Call inference_service (http://localhost:8001/generate) over HTTP to structure fields into JSON
       - Supports "fast" mode (OCR text -> qwen3:4b-instruct, ~5-15s latency on CPU)
       - Supports "vlm" mode (Image base64 -> gemma3:4b vision-language, ~30-60s latency on CPU)

Run:
    ..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8002
"""

import os
import tempfile
import base64
import json
import re
import time
from typing import List, Dict, Any, Optional

import httpx
from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from paddleocr import PaddleOCR

INFERENCE_SERVICE_URL = "http://localhost:8001/generate"
INFERENCE_HEALTH_URL = "http://localhost:8001/health"

app = FastAPI(title="Sovereign Workbench - Multimodal API", version="0.1.0")

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy singleton PaddleOCR engine
ocr_engine = None

def get_ocr_engine():
    global ocr_engine
    if ocr_engine is None:
        ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
    return ocr_engine


# ---------- Contract Schemas ----------

class OCRLine(BaseModel):
    text: str
    confidence: float
    bbox: Optional[List[Any]] = None


class AnalyzeResponse(BaseModel):
    page_ref: str
    ocr_text: str
    ocr_lines: List[OCRLine]
    ocr_avg_confidence: float
    structured_fields: Dict[str, Any]
    vlm_raw_response: str
    execution_time_ms: int
    mode_used: str


@app.get("/", response_class=FileResponse)
def read_root():
    """Serves the Sovereign Multimodal Demo Dashboard UI."""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Sovereign Multimodal Service Running (port 8002)</h1>")


@app.get("/health")
def health():
    return {"status": "ok", "ocr_ready": ocr_engine is not None}


@app.post("/generate")
async def proxy_generate(request: Request):
    """Proxy POST /generate to inference_service (port 8001) for robust single-origin UI fetch."""
    body = await request.json()
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            resp = await client.post(INFERENCE_SERVICE_URL, json=body)
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Inference proxy error: {e}")


def parse_json_from_llm(raw_text: str) -> Dict[str, Any]:
    """Helper to extract clean JSON object from LLM raw markdown output."""
    if not raw_text:
        return {}
    
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = raw_text[start:end+1]
        else:
            json_str = raw_text

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"raw_unparsed": raw_text.strip()}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    mode: str = Query("fast", description="Processing mode: 'fast' (CPU optimized, OCR+LLM) or 'vlm' (Direct Vision Gemma3)")
):
    start_time = time.time()
    
    suffix = os.path.splitext(file.filename or "doc.png")[1]
    if not suffix:
        suffix = ".png"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # 1. Run PaddleOCR
        engine = get_ocr_engine()
        ocr_result = engine.ocr(tmp_path, cls=True)

        lines: List[OCRLine] = []
        full_text_list = []
        confidences = []

        if ocr_result and len(ocr_result) > 0 and ocr_result[0] is not None:
            for item in ocr_result[0]:
                bbox = item[0]
                text, conf = item[1]
                lines.append(OCRLine(text=text, confidence=round(float(conf), 4), bbox=bbox))
                full_text_list.append(text)
                confidences.append(float(conf))

        ocr_text = "\n".join(full_text_list)
        avg_confidence = round(sum(confidences) / len(confidences), 4) if confidences else 0.0

        img_b64 = base64.b64encode(contents).decode("utf-8")

        # 2. Call inference_service over HTTP
        structured_fields = {}
        vlm_raw_response = ""
        actual_mode = mode

        async with httpx.AsyncClient(timeout=180.0) as client:
            if mode == "vlm":
                prompt = (
                    "Analyze this document image and extract all key data fields as a valid JSON object. "
                    "Keys should be normalized field names (e.g. document_type, date, status, total_amount, metadata). "
                    "Return ONLY valid JSON."
                )
                payload = {
                    "model_id": "gemma3:4b",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                            "images": [img_b64]
                        }
                    ],
                    "config": {"temperature": 0.1, "max_tokens": 1024}
                }
            else:
                prompt = (
                    f"Extract key structured fields from this OCR text into a JSON object.\n"
                    f"OCR Text:\n{ocr_text}\n\n"
                    f"Return ONLY a clean JSON object with extracted key-value pairs."
                )
                payload = {
                    "model_id": "qwen3:4b-instruct-2507-q4_K_M",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "config": {"temperature": 0.1, "max_tokens": 1024}
                }

            try:
                resp = await client.post(INFERENCE_SERVICE_URL, json=payload)
                resp.raise_for_status()
                gen_data = resp.json()
                vlm_raw_response = gen_data.get("response", "")
                structured_fields = parse_json_from_llm(vlm_raw_response)
            except Exception as e:
                # Fallback if preferred model call fails
                if mode == "vlm":
                    actual_mode = "fast_fallback"
                    fallback_payload = {
                        "model_id": "qwen3:4b-instruct-2507-q4_K_M",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Extract structured key-value JSON from this OCR text:\n{ocr_text}"
                            }
                        ]
                    }
                    try:
                        resp = await client.post(INFERENCE_SERVICE_URL, json=fallback_payload)
                        gen_data = resp.json()
                        vlm_raw_response = gen_data.get("response", "")
                        structured_fields = parse_json_from_llm(vlm_raw_response)
                    except Exception as fb_err:
                        vlm_raw_response = f"Inference call error: {e} | Fallback error: {fb_err}"
                        structured_fields = {"error": str(e)}
                else:
                    vlm_raw_response = f"Inference service error: {e}"
                    structured_fields = {"error": str(e)}

        exec_time = int((time.time() - start_time) * 1000)

        return AnalyzeResponse(
            page_ref=f"file://{file.filename or 'upload.png'}",
            ocr_text=ocr_text,
            ocr_lines=lines,
            ocr_avg_confidence=avg_confidence,
            structured_fields=structured_fields,
            vlm_raw_response=vlm_raw_response,
            execution_time_ms=exec_time,
            mode_used=actual_mode
        )

    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
