from pathlib import Path


class SandboxPolicy:

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()

    def is_path_allowed(self, path: Path) -> bool:
        try:
            path.resolve().relative_to(self.workspace)
            return True
        except ValueError:
            return False

    def check_path(self, path: Path):
        if not self.is_path_allowed(path):
            raise PermissionError(
                "Access denied: path is outside sandbox workspace"
            )