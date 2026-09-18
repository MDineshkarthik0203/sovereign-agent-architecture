from pathlib import Path

from execution_backend import ExecutionBackend
from runner import run_code


class LocalPythonBackend(ExecutionBackend):

    def execute(
        self,
        code: str,
        workspace_path: Path,
        timeout: int = 5
    ):
        return run_code(
            code=code,
            workspace_path=workspace_path,
            timeout=timeout
        )