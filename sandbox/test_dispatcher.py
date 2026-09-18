from dispatcher import ToolDispatcher
from tool_registry import ToolRegistry


def add(a, b):
    return a + b


def greet(name):
    return f"Hello, {name}!"


registry = ToolRegistry()

registry.register("add", add)
registry.register("greet", greet)

dispatcher = ToolDispatcher(registry)


# Test tool with arguments
result = dispatcher.dispatch(
    "add",
    {"a": 10, "b": 20}
)

print("Add result:", result)


# Test another tool
result = dispatcher.dispatch(
    "greet",
    {"name": "Sameer"}
)

print("Greet result:", result)


# Test missing arguments
try:
    dispatcher.dispatch("add")
except TypeError as e:
    print("Missing arguments detected:", e)


# Test invalid argument type
try:
    dispatcher.dispatch("add", ["10", "20"])
except TypeError as e:
    print("Invalid arguments blocked:", e)


# Test unknown tool
try:
    dispatcher.dispatch("unknown", {})
except KeyError as e:
    print("Unknown tool blocked:", e)