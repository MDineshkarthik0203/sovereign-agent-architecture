from .tool_registry import ToolRegistry


class ToolDispatcher:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def dispatch(
        self,
        tool_name: str,
        args: dict | None = None
    ):
        if args is None:
            args = {}

        # Get the registered tool
        tool = self.registry.get(tool_name)

        # Get its argument schema
        schema = self.registry.get_schema(
            tool_name
        )

        # Validate arguments before execution
        schema.validate(args)

        # Execute the tool
        return tool(**args)