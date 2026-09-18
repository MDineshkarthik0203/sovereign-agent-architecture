from tool_registry import ToolRegistry


def hello_tool():
    return "Hello from tool"


registry = ToolRegistry()

# Register a tool
registry.register("hello", hello_tool)

# Get the tool
tool = registry.get("hello")

# Execute the tool
result = tool()

print("Tool result:", result)

# List registered tools
print("Registered tools:", registry.list_tools())

# Test duplicate registration
try:
    registry.register("hello", hello_tool)
except ValueError as e:
    print("Duplicate registration blocked:", e)

# Test unknown tool
try:
    registry.get("unknown")
except KeyError as e:
    print("Unknown tool blocked:", e)