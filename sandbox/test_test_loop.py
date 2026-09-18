from test_loop import TestLoop
from workspace import SandboxWorkspace


workspace_manager = SandboxWorkspace()
workspace_path = workspace_manager.create()

try:
    test_loop = TestLoop(workspace_path)

    # -----------------------------
    # TEST 1: Passing test
    # -----------------------------

    code = """
def add(a, b):
    return a + b
"""

    tests = """
exec(open("main.py").read())

assert add(10, 20) == 30

print("ALL TESTS PASSED")
"""

    result = test_loop.run(
        code=code,
        tests=tests
    )

    print("PASSING TEST RESULT:")
    print(result)

    # -----------------------------
    # TEST 2: Failing test
    # -----------------------------

    code = """
def add(a, b):
    return a - b
"""

    tests = """
exec(open("main.py").read())

assert add(10, 20) == 30

print("ALL TESTS PASSED")
"""

    result = test_loop.run(
        code=code,
        tests=tests
    )

    print("\nFAILING TEST RESULT:")
    print(result)

finally:
    workspace_manager.cleanup()