from pathlib import Path

from file_tools import FileTools
from workspace import SandboxWorkspace


workspace = SandboxWorkspace()
workspace_path = workspace.create()

try:
    tools = FileTools(workspace_path)

    try:
        tools.write_file(
            "../escape_test.txt",
            "This should NOT be allowed"
        )

        print("SECURITY FAILURE: escape was allowed")

    except PermissionError as e:
        print("SECURITY TEST PASSED")
        print(e)

finally:
    workspace.cleanup()