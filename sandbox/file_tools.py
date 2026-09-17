from pathlib import Path

from .policy import SandboxPolicy


class FileTools:

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.policy = SandboxPolicy(self.workspace)

    def read_file(self, path: str) -> str:
        file_path = (self.workspace / path).resolve()

        self.policy.check_path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"Not a file: {path}")

        return file_path.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str):
        file_path = (self.workspace / path).resolve()

        self.policy.check_path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "status": "success",
            "path": str(file_path)
        }