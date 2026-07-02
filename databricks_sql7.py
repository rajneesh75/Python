# -----------------------
# TOOL 2: evaluate math expression
# -----------------------
def calculate_math_expression(expression: str) -> float:
    """
    Evaluates a basic math expression safely.

    Args:
        expression (str): A math expression (e.g., "sqrt(2 + 3 * (4 - 1)), using python math functions.").

    Returns:
        float: The result of the evaluated expression.
    """
    import math
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"abs": abs, "round": round})

    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")


print(calculate_math_expression("6 + 3 * (13 - 1)/2"))
