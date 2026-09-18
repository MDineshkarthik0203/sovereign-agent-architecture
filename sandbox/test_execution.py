from sandbox import Sandbox


sandbox = Sandbox()

try:
    sandbox.write_file(
        "input.txt",
        "Hello from the shared workspace!"
    )

    result = sandbox.execute("""
from pathlib import Path

content = Path("input.txt").read_text()

print(content)
""")

    print(result)

finally:
    sandbox.cleanup()