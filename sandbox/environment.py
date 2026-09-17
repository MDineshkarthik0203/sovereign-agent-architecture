import os


def build_environment():
    """
    Build a clean environment for sandboxed code execution.
    """

    environment = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
    }

    return environment