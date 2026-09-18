import subprocess
import sys
import time
from pathlib import Path


class TestLoop:

    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(workspace_path).resolve()

    def run(
        self,
        code: str,
        tests: str,
        timeout: int = 5
    ):
        # Save user's code
        code_file = self.workspace_path / "main.py"

        code_file.write_text(
            code,
            encoding="utf-8"
        )

        # Save test code
        test_file = self.workspace_path / "test_main.py"

        test_file.write_text(
            tests,
            encoding="utf-8"
        )

        start_time = time.time()

        try:
            process = subprocess.run(
                [
                    sys.executable,
                    str(test_file)
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace_path
            )

            execution_time = time.time() - start_time

            return {
                "status": (
                    "passed"
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
                "stderr": "Test execution timed out",
                "exit_code": None,
                "execution_time": execution_time
            }