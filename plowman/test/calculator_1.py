def calculate(expression):

    """
    Evaluates a mathematical expression string with support for addition, subtraction,
    multiplication, division, parentheses, and operator precedence.

    Args:
      expression: A string representing the mathematical expression.
      
    Returns:
      The result of the evaluated expression.

    Raises:
      ValueError: If the expression is invalid (e.g., misplaced operators or parentheses).
    """

    if not expression:

        return ""

    def find_closing_parenthesis(expr, start_index):

        """Helper function to find the matching closing parenthesis."""

        count = 1

        for i in range(start_index + 1, len(expr)):

            if expr[i] == "(":

                count += 1

            elif expr[i] == ")":

                count -= 1

                if count == 0:

                    return i

        raise ValueError("Mismatched parentheses")

    def evaluate_simple_expression(expr):

        """Helper function to evaluate a simple expression without parentheses."""

        parts = []

        current_number = ""

        current_operator = "+"

        for char in expr:

            if char.isdigit() or char == ".":

                current_number += char

            elif char in "+-*/":

                parts.append(
                    (current_operator, float(current_number) if current_number else 0.0)
                )

                current_number = ""

                current_operator = char

            else:

                raise ValueError("Invalid character in expression")

        parts.append(
            (current_operator, float(current_number) if current_number else 0.0)
        )

        result = 0.0

        i = 0

        while i < len(parts):

            operator, number = parts[i]

            if operator == "+":

                result += number

            elif operator == "-":

                result -= number

            elif operator == "*":

                if i + 1 < len(parts):

                    result *= parts[i + 1][1]

                    i += 1

                else:

                    raise ValueError("Invalid expression")

            elif operator == "/":

                if i + 1 < len(parts):

                    if parts[i + 1][1] == 0:

                        raise ValueError("Division by zero")

                    result /= parts[i + 1][1]

                    i += 1

                else:

                    raise ValueError("Invalid expression")

            i += 1

        return result

    index = 0

    result = 0.0

    current_operator = "+"

    while index < len(expression):

        char = expression[index]

        if char.isdigit() or char == ".":

            start = index

            while index < len(expression) and (
                expression[index].isdigit() or expression[index] == "."
            ):

                index += 1

            number = float(expression[start:index])

            if current_operator == "+":

                result += number

            elif current_operator == "-":

                result -= number

            elif current_operator == "*":

                result *= number

            elif current_operator == "/":

                if number == 0:

                    raise ValueError("Division by zero")

                result /= number

        elif char in "+-":

            current_operator = char

            index += 1

        elif char in "*/":

            current_operator = char

            index += 1

        elif char == "(":

            end = find_closing_parenthesis(expression, index)

            sub_expr = expression[index + 1 : end]

            sub_result = calculate(sub_expr)

            if current_operator == "+":

                result += sub_result

            elif current_operator == "-":

                result -= sub_result

            elif current_operator == "*":

                result *= sub_result

            elif current_operator == "/":

                if sub_result == 0:

                    raise ValueError("Division by zero")

                result /= sub_result

            index = end + 1

        else:

            raise ValueError("Invalid character in expression")

    if expression.isdigit() or (
        expression.startswith("-") and expression[1:].replace(".", "", 1).isdigit()
    ):

        return float(expression)

    return result

def main():
    test_expressions = [
        "3+5",                  # Simple addition
        "100-50*5",               # Operator precedence
        "10/(2+3)",             # Division with parentheses
        "3*(2+1)",              # Multiplication with parentheses
        "3.5+2.5",              # Decimal numbers
        "4*(3+2*(1+1))",        # Nested parentheses
        "((1+2)*(3-1))/2",      # Deeply nested with division
        "",                     # Empty string
        "3/0",                  # Division by zero (should raise error)
        "5+*2",                 # Invalid expression (misplaced operator)
        "(3+2",                 # Mismatched parentheses
    ]

    for expr in test_expressions:
        try:
            result = calculate(expr)
            print(f"Expression: {expr} => Result: {result}")
        except Exception as e:
            print(f"Expression: {expr} => Error: {e}")

if __name__ == "__main__":
    main()
