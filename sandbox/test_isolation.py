from pathlib import Path
from sandbox import Sandbox


sandbox = Sandbox()

try:
    # Create a file OUTSIDE the sandbox workspace
    outside_file = sandbox.workspace_path.parent / "outside_test.txt"
    outside_file.write_text("SECRET OUTSIDE SANDBOX", encoding="utf-8")

    # Ask sandboxed code to access it
    code = """
from pathlib import Path

outside = Path("..") / "outside_test.txt"

try:
    print(outside.read_text())
except Exception as e:
    print("BLOCKED:", type(e).__name__)
"""

    result = sandbox.execute(code)

    print("Execution result:")
    print(result)

finally:
    sandbox.cleanup()

    if outside_file.exists():
        outside_file.unlink()