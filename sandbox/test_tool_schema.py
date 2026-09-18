from sandbox import Sandbox


sandbox = Sandbox()

try:
    # Missing required argument
    try:
        sandbox.dispatcher.dispatch(
            "read_file",
            {}
        )
    except ValueError as e:
        print("MISSING ARGUMENT BLOCKED:", e)

    # Unexpected argument
    try:
        sandbox.dispatcher.dispatch(
            "read_file",
            {
                "path": "hello.txt",
                "unexpected": "blocked"
            }
        )
    except ValueError as e:
        print("UNEXPECTED ARGUMENT BLOCKED:", e)

    # Valid argument
    sandbox.dispatcher.dispatch(
        "write_file",
        {
            "path": "test.txt",
            "content": "Schema validation works!"
        }
    )

    result = sandbox.dispatcher.dispatch(
        "read_file",
        {
            "path": "test.txt"
        }
    )

    print("VALID CALL:", result)

finally:
    sandbox.cleanup()