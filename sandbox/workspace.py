import tempfile
import shutil
from pathlib import Path


class SandboxWorkspace:

    def __init__(self):
        self.path = None

    def create(self):
        self.path = Path(
            tempfile.mkdtemp(prefix="sih_sandbox_")
        )

        return self.path

    def cleanup(self):
        if self.path and self.path.exists():
            shutil.rmtree(self.path, ignore_errors=True)