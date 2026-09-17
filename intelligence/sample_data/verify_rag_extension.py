import os
import sys
import time
import json
import httpx
import subprocess

def test_multimodal_pipeline():
    print("\n--- 1. Running Multimodal & Inference Pipeline Verification ---")
    script_path = os.path.join(os.path.dirname(__file__), "verify_pipeline.py")
    res = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    print(res.stdout)
    assert res.returncode == 0, f"Pipeline verification failed: {res.stderr}"
    print("[OK] Existing Multimodal Pipeline & Inference Service test passed cleanly.")

def test_generate_without_context():
    print("\n--- 2. Testing /generate Without Context (Backward Compatibility) ---")
    url = "http://localhost:8001/generate"
    payload = {
        "model_id": "qwen3:4b-instruct-2507-q4_K_M",
        "messages": [
            {"role": "user", "content": "Say hello in 3 words."}
        ]
    }
    start = time.time()
    resp = httpx.post(url, json=payload, timeout=60.0)
    latency = round(time.time() - start, 2)
    print(f"Status Code: {resp.status_code}")
    print(f"Latency: {latency}s")
    data = resp.json()
    print("Response Body:", json.dumps(data, indent=2))
    assert resp.status_code == 200
    assert "sources" not in data or data["sources"] is None
    print("[OK] Backward compatibility test passed: No 'sources' returned when context is omitted.")

def test_generate_with_mock_rag_context():
    print("\n--- 3. Testing /generate With Mock Local-RAG Context ---")
    url = "http://localhost:8001/generate"
    payload = {
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
                    "content": "Cooling System Specification: The recommended system operating pressure for Air-Gapped Workbench Node A is strictly 101.3 kPa."
                }
            ]
        }
    }
    start = time.time()
    resp = httpx.post(url, json=payload, timeout=60.0)
    latency = round(time.time() - start, 2)
    print(f"Status Code: {resp.status_code}")
    print(f"Latency: {latency}s")
    data = resp.json()
    print("Response Body:", json.dumps(data, indent=2))
    assert resp.status_code == 200
    assert "sources" in data and data["sources"] is not None
    assert len(data["sources"]) == 1
    assert data["sources"][0]["document"] == "Sovereign_Node_Specs.pdf"
    assert data["sources"][0]["page"] == 24
    print("[OK] RAG Grounded Context & Source Attribution test passed cleanly.")

if __name__ == "__main__":
    print("==========================================================")
    print("SIH 2026 RAG-READY INTELLIGENCE SERVICE EXTENSION VERIFICATION")
    print("==========================================================")
    test_generate_without_context()
    test_generate_with_mock_rag_context()
    test_multimodal_pipeline()
    print("\n=== ALL RAG EXTENSION & BACKWARD COMPATIBILITY TESTS PASSED! ===")
