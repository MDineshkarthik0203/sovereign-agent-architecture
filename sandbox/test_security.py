from pathlib import Path

from artifact_generator import ArtifactGenerator
from sandbox import Sandbox


sandbox = Sandbox()

try:
    print("=== SECURITY TESTS ===")

    # -------------------------------------------------
    # 1. FileTools path traversal
    # -------------------------------------------------

    print("\n[1] File path traversal")

    try:
        sandbox.write_file(
            "../escape_test.txt",
            "should not be written"
        )

        print("FAIL: Path traversal was allowed")

    except PermissionError:
        print("PASS: Path traversal blocked")

    # -------------------------------------------------
    # 2. Artifact path traversal
    # -------------------------------------------------

    print("\n[2] Artifact path traversal")

    try:
        sandbox.generate_artifact(
            "../escape_artifact.txt",
            "should not be written"
        )

        print("FAIL: Artifact traversal was allowed")

    except PermissionError:
        print("PASS: Artifact traversal blocked")

    # -------------------------------------------------
    # 3. Unknown tool
    # -------------------------------------------------

    print("\n[3] Unknown tool")

    try:
        sandbox.dispatcher.dispatch(
            "unknown_tool",
            {}
        )

        print("FAIL: Unknown tool was executed")

    except KeyError:
        print("PASS: Unknown tool blocked")

    # -------------------------------------------------
    # 4. Unexpected arguments
    # -------------------------------------------------

    print("\n[4] Unexpected arguments")

    try:
        sandbox.dispatcher.dispatch(
            "read_file",
            {
                "path": "test.txt",
                "unexpected": True
            }
        )

        print("FAIL: Unexpected argument accepted")

    except ValueError:
        print("PASS: Unexpected argument blocked")

    # -------------------------------------------------
    # 5. Missing arguments
    # -------------------------------------------------

    print("\n[5] Missing arguments")

    try:
        sandbox.dispatcher.dispatch(
            "write_file",
            {
                "path": "test.txt"
            }
        )

        print("FAIL: Missing argument accepted")

    except ValueError:
        print("PASS: Missing argument blocked")

    # -------------------------------------------------
    # 6. Invalid argument type
    # -------------------------------------------------

    print("\n[6] Invalid argument type")

    try:
        sandbox.dispatcher.dispatch(
            "read_file",
            ["test.txt"]
        )

        print("FAIL: Invalid argument type accepted")

    except TypeError:
        print("PASS: Invalid argument type blocked")

    # -------------------------------------------------
    # 7. Execution timeout
    # -------------------------------------------------

    print("\n[7] Execution timeout")

    result = sandbox.execute(
        """
while True:
    pass
""",
        timeout=2
    )

    if result["status"] == "timeout":
        print("PASS: Execution timeout enforced")
    else:
        print("FAIL: Execution timeout not enforced")

    # -------------------------------------------------
    # 8. Valid operation
    # -------------------------------------------------

    print("\n[8] Valid operation")

    result = sandbox.write_file(
        "security_test.txt",
        "Security test successful"
    )

    content = sandbox.read_file(
        "security_test.txt"
    )

    if (
        result["status"] == "success"
        and content == "Security test successful"
    ):
        print("PASS: Valid file operation works")
    else:
        print("FAIL: Valid file operation failed")

    print("\n=== SECURITY TESTS COMPLETED ===")

finally:
    sandbox.cleanup()