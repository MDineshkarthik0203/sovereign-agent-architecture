from sandbox import Sandbox


sandbox = Sandbox()

try:
    # Test write_file through the dispatcher
    write_result = sandbox.dispatcher.dispatch(
        "write_file",
        {
            "path": "hello.txt",
            "content": "Hello from the tool registry!"
        }
    )

    print("WRITE:", write_result)

    # Test read_file through the dispatcher
    read_result = sandbox.dispatcher.dispatch(
        "read_file",
        {
            "path": "hello.txt"
        }
    )

    print("READ:", read_result)

    # Test execute_code through the dispatcher
    execution_result = sandbox.dispatcher.dispatch(
        "execute_code",
        {
            "code": "print('Hello from execute_code tool!')"
        }
    )

    print("EXECUTE:", execution_result)

    # Show registered tools
    print("TOOLS:", sandbox.registry.list_tools())

finally:
    sandbox.cleanup()