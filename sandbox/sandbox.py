from pathlib import Path
import shutil

from .artifact_generator import ArtifactGenerator
from .dispatcher import ToolDispatcher
from .file_tools import FileTools
from .local_backend import LocalPythonBackend
from .tool_registry import ToolRegistry
from .tool_schema import ToolSchema
from .workspace import SandboxWorkspace


class Sandbox:

    def __init__(self):

        # ========================================================
        # WORKSPACE
        # ========================================================

        self.workspace_manager = SandboxWorkspace()
        self.workspace_path = self.workspace_manager.create()


        # ========================================================
        # FILE TOOLS
        # ========================================================

        self.file_tools = FileTools(
            self.workspace_path
        )


        # ========================================================
        # EXECUTION BACKEND
        # ========================================================

        self.backend = LocalPythonBackend()


        # ========================================================
        # ARTIFACT GENERATOR
        # ========================================================

        self.artifact_generator = ArtifactGenerator(
            self.workspace_path
        )


        # ========================================================
        # TOOL REGISTRY
        # ========================================================

        self.registry = ToolRegistry()


        # ========================================================
        # TOOL DISPATCHER
        # ========================================================

        self.dispatcher = ToolDispatcher(
            self.registry
        )


        # ========================================================
        # REGISTER TOOLS
        # ========================================================

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


    # ============================================================
    # STAGE INPUT FILE INTO SANDBOX
    # ============================================================

    def stage_file(
        self,
        source_path: str,
        sandbox_path: str | None = None
    ):
        """
        Copy an input file into the controlled Sandbox workspace.

        The agent/tools can then access the staged copy
        through FileTools and SandboxPolicy.
        """

        source = Path(source_path).expanduser().resolve()

        if not source.exists():
            raise FileNotFoundError(
                f"Input file not found: {source_path}"
            )

        if not source.is_file():
            raise IsADirectoryError(
                f"Input path is not a file: {source_path}"
            )

        destination_name = (
            sandbox_path
            if sandbox_path
            else source.name
        )

        destination = (
            self.workspace_path / destination_name
        ).resolve()

        # Prevent staging outside the Sandbox workspace
        if self.workspace_path not in destination.parents:
            raise PermissionError(
                "Sandbox input path escapes the workspace."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            source,
            destination
        )

        return {
            "status": "success",
            "source": str(source),
            "sandbox_path": str(destination)
        }


    # ============================================================
    # EXECUTE CODE
    # ============================================================

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


    # ============================================================
    # READ FILE
    # ============================================================

    def read_file(
        self,
        path: str
    ):

        return self.file_tools.read_file(
            path
        )


    # ============================================================
    # WRITE FILE
    # ============================================================

    def write_file(
        self,
        path: str,
        content: str
    ):

        return self.file_tools.write_file(
            path=path,
            content=content
        )


    # ============================================================
    # GENERATE ARTIFACT
    # ============================================================

    def generate_artifact(
        self,
        filename: str,
        content: str
    ):

        return self.artifact_generator.generate_text(
            filename=filename,
            content=content
        )


    # ============================================================
    # LIST TOOLS
    # ============================================================

    def list_tools(self):

        return self.registry.list_tools()


    # ============================================================
    # CALL TOOL
    # ============================================================

    def call_tool(
        self,
        tool_name: str,
        args: dict | None = None
    ):

        return self.dispatcher.dispatch(
            tool_name=tool_name,
            args=args
        )


    # ============================================================
    # CLEANUP
    # ============================================================

    def cleanup(self):

        self.workspace_manager.cleanup()