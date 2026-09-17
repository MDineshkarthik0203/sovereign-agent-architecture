import os
import time
import json
import httpx

def test_inference_service():
    print("\n--- 1. Testing Inference Service (Port 8001) ---")
    url = "http://localhost:8001/generate"
    payload = {
        "model_id": "qwen3:4b-instruct-2507-q4_K_M",
        "messages": [
            {"role": "user", "content": "Reply with a JSON object containing key 'status' with value 'active' and 'message' with value 'Inference API OK'."}
        ]
    }
    start = time.time()
    resp = httpx.post(url, json=payload, timeout=60.0)
    latency = round(time.time() - start, 2)
    print(f"Status Code: {resp.status_code}")
    print(f"Response Latency: {latency}s")
    print(f"Response Body: {json.dumps(resp.json(), indent=2)}")
    assert resp.status_code == 200

def test_multimodal_fast_mode():
    print("\n--- 2. Testing Multimodal Service - Fast CPU Mode (Port 8002) ---")
    url = "http://localhost:8002/analyze?mode=fast"
    img_path = os.path.join(os.path.dirname(__file__), "test_report.png")
    
    start = time.time()
    with open(img_path, "rb") as f:
        files = {"file": ("test_report.png", f, "image/png")}
        resp = httpx.post(url, files=files, timeout=120.0)
    latency = round(time.time() - start, 2)

    print(f"Status Code: {resp.status_code}")
    print(f"Pipeline Latency: {latency}s")
    data = resp.json()
    print("Extracted OCR Text Preview:")
    print("-" * 40)
    print(data.get("ocr_text"))
    print("-" * 40)
    print(f"OCR Average Confidence: {data.get('ocr_avg_confidence')}")
    print(f"Mode Used: {data.get('mode_used')}")
    print("Structured Fields Output:")
    print(json.dumps(data.get("structured_fields"), indent=2))
    assert resp.status_code == 200
    assert data.get("ocr_avg_confidence", 0) > 0.8
    assert len(data.get("ocr_lines", [])) > 0

def test_multimodal_vlm_mode():
    print("\n--- 3. Testing Multimodal Service - VLM Gemma3 Direct Mode (Port 8002) ---")
    url = "http://localhost:8002/analyze?mode=vlm"
    img_path = os.path.join(os.path.dirname(__file__), "test_report.png")
    
    start = time.time()
    with open(img_path, "rb") as f:
        files = {"file": ("test_report.png", f, "image/png")}
        resp = httpx.post(url, files=files, timeout=180.0)
    latency = round(time.time() - start, 2)

    print(f"Status Code: {resp.status_code}")
    print(f"Pipeline Latency: {latency}s")
    data = resp.json()
    print(f"Mode Used: {data.get('mode_used')}")
    print("Structured Fields Output:")
    print(json.dumps(data.get("structured_fields"), indent=2))
    assert resp.status_code == 200

if __name__ == "__main__":
    print("Starting Sovereign Workbench End-to-End Pipeline Verification...")
    test_inference_service()
    test_multimodal_fast_mode()
    test_multimodal_vlm_mode()
    print("\n=== ALL PIPELINE VERIFICATION TESTS PASSED SUCCESSFULLY! ===")
