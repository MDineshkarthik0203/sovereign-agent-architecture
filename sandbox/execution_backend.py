from abc import ABC, abstractmethod
from pathlib import Path


class ExecutionBackend(ABC):

    @abstractmethod
    def execute(
        self,
        code: str,
        workspace_path: Path,
        timeout: int = 5
    ):
        pass