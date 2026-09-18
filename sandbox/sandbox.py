from artifact_generator import ArtifactGenerator
from dispatcher import ToolDispatcher
from file_tools import FileTools
from local_backend import LocalPythonBackend
from tool_registry import ToolRegistry
from tool_schema import ToolSchema
from workspace import SandboxWorkspace


class Sandbox:

    def __init__(self):
        # Workspace
        self.workspace_manager = SandboxWorkspace()
        self.workspace_path = self.workspace_manager.create()

        # File tools
        self.file_tools = FileTools(
            self.workspace_path
        )

        # Execution backend
        self.backend = LocalPythonBackend()

        # Artifact generator
        self.artifact_generator = ArtifactGenerator(
            self.workspace_path
        )

        # Tool registry
        self.registry = ToolRegistry()

        # Tool dispatcher
        self.dispatcher = ToolDispatcher(
            self.registry
        )

        # Register tools
        self.registry.register(
            "read_file",
            self.read_file,
            ToolSchema(
                required_args=["path"]
            )
        )

        self.registry.register(
            "write_file",
            self.write_file,
            ToolSchema(
                required_args=["path", "content"]
            )
        )

        self.registry.register(
            "execute_code",
            self.execute,
            ToolSchema(
                required_args=["code"],
                optional_args=["timeout"]
            )
        )

        self.registry.register(
            "generate_artifact",
            self.generate_artifact,
            ToolSchema(
                required_args=["filename", "content"]
            )
        )

    def execute(
        self,
        code: str,
        timeout: int = 5
    ):
        return self.backend.execute(
            code=code,
            workspace_path=self.workspace_path,
            timeout=timeout
        )

    def read_file(
        self,
        path: str
    ):
        return self.file_tools.read_file(
            path
        )

    def write_file(
        self,
        path: str,
        content: str
    ):
        return self.file_tools.write_file(
            path=path,
            content=content
        )

    def generate_artifact(
        self,
        filename: str,
        content: str
    ):
        return self.artifact_generator.generate_text(
            filename=filename,
            content=content
        )

    def list_tools(self):
        return self.registry.list_tools()

    def call_tool(
        self,
        tool_name: str,
        args: dict | None = None
    ):
        return self.dispatcher.dispatch(
            tool_name=tool_name,
            args=args
        )

    def cleanup(self):
        self.workspace_manager.cleanup()