# M5 Sandbox & Tool Service

This directory contains the M5 Tools / Sandbox component for the
Sovereign On-Premise Agentic AI Workbench.

## Responsibilities

M5 provides:

- Sandbox workspace management
- Python code execution
- Execution timeout handling
- Controlled file read/write operations
- Workspace path permission policy
- Tool registry
- Tool dispatcher
- Tool argument validation
- Test execution loop
- Artifact generation

## Available Tools

### read_file

Reads a file inside the sandbox workspace.

Arguments:

- `path`

### write_file

Writes a file inside the sandbox workspace.

Arguments:

- `path`
- `content`

### execute_code

Executes Python code using the configured execution backend.

Arguments:

- `code`
- `timeout` (optional)

### generate_artifact

Generates a text artifact inside the sandbox workspace.

Arguments:

- `filename`
- `content`

## Public API

```python
from sandbox import Sandbox

sandbox = Sandbox()

try:
    sandbox.call_tool(
        "write_file",
        {
            "path": "hello.txt",
            "content": "Hello from M5!"
        }
    )

    result = sandbox.call_tool(
        "execute_code",
        {
            "code": "print('Hello')"
        }
    )

    print(result)

finally:
    sandbox.cleanup()