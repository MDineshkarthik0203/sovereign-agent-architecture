from .tool_schema import ToolSchema


class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(
        self,
        name: str,
        tool,
        schema: ToolSchema | None = None
    ):
        if not name:
            raise ValueError(
                "Tool name cannot be empty"
            )

        if name in self._tools:
            raise ValueError(
                f"Tool already registered: {name}"
            )

        if schema is None:
            schema = ToolSchema()

        self._tools[name] = {
            "tool": tool,
            "schema": schema
        }

    def get(self, name: str):
        if name not in self._tools:
            raise KeyError(
                f"Tool not found: {name}"
            )

        return self._tools[name]["tool"]

    def get_schema(self, name: str):
        if name not in self._tools:
            raise KeyError(
                f"Tool not found: {name}"
            )

        return self._tools[name]["schema"]

    def list_tools(self):
        return list(self._tools.keys())