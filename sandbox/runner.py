import subprocess
import sys
import time
from pathlib import Path
from .environment import build_environment

def run_code(
    code: str,
    workspace_path: Path,
    timeout: int = 5
):
    workspace_path = Path(workspace_path).resolve()

    code_file = workspace_path / "main.py"

    code_file.write_text(
        code,
        encoding="utf-8"
    )

    start_time = time.time()

    try:
        process = subprocess.run(
        [sys.executable, str(code_file)],
         capture_output=True,
        text=True,
         timeout=timeout,
        cwd=workspace_path,
        env=build_environment()
)
        execution_time = time.time() - start_time

        return {
            "status": (
                "success"
                if process.returncode == 0
                else "failed"
            ),
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:

        execution_time = time.time() - start_time

        return {
            "status": "timeout",
            "stdout": "",
            "stderr": "Execution timed out",
            "exit_code": None,
            "execution_time": execution_time
        }