def calculator(expression: str) -> str:
    """
    Simple calculator tool for basic arithmetic expressions.
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"