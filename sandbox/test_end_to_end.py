from sandbox import Sandbox
from test_loop import TestLoop


sandbox = Sandbox()

try:
    # -------------------------------------------------
    # 1. Initial buggy code
    # -------------------------------------------------

    buggy_code = """
def add(a, b):
    return a - b
"""

    # -------------------------------------------------
    # 2. Test that should fail
    # -------------------------------------------------

    tests = """
exec(open("main.py").read())

assert add(10, 20) == 30

print("ALL TESTS PASSED")
"""

    test_loop = TestLoop(
        sandbox.workspace_path
    )

    print("=== FIRST TEST RUN ===")

    result = test_loop.run(
        code=buggy_code,
        tests=tests
    )

    print(result)

    if result["status"] != "failed":
        raise RuntimeError(
            "Expected the first test to fail"
        )

    print("FIRST TEST: FAILED AS EXPECTED")

    # -------------------------------------------------
    # 3. Simulate agent repairing the code
    # -------------------------------------------------

    repaired_code = """
def add(a, b):
    return a + b
"""

    print("\n=== REPAIRED TEST RUN ===")

    result = test_loop.run(
        code=repaired_code,
        tests=tests
    )

    print(result)

    if result["status"] != "passed":
        raise RuntimeError(
            "Expected the repaired test to pass"
        )

    print("SECOND TEST: PASSED")

    # -------------------------------------------------
    # 4. Generate final artifact
    # -------------------------------------------------

    artifact_result = sandbox.dispatcher.dispatch(
        "generate_artifact",
        {
            "filename": "final_report.txt",
            "content": (
                "Sandbox Test Report\n\n"
                "Initial test: FAILED\n"
                "Code repaired: YES\n"
                "Final test: PASSED\n"
                "Artifact generation: SUCCESS\n"
            )
        }
    )

    print("\n=== ARTIFACT ===")
    print(artifact_result)

    # -------------------------------------------------
    # 5. Verify artifact
    # -------------------------------------------------

    artifact_content = sandbox.read_file(
        "final_report.txt"
    )

    print("\n=== ARTIFACT CONTENT ===")
    print(artifact_content)

    print("\n=== END-TO-END TEST PASSED ===")

finally:
    sandbox.cleanup()