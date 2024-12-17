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

      if expr[i] == '(':

        count += 1

      elif expr[i] == ')':

        count -= 1

        if count == 0:

          return i

    raise ValueError("Mismatched parentheses")



  def evaluate_expression(expr):

    """Evaluates the expression considering operator precedence."""

    nums = []

    ops = []

    i = 0



    def compute():

      if not nums or not ops:

        return

      num2 = nums.pop()

      num1 = nums.pop()

      op = ops.pop()

      if op == '+':

        nums.append(num1 + num2)

      elif op == '-':

        nums.append(num1 - num2)

      elif op == '*':

        nums.append(num1 * num2)

      elif op == '/':

        if num2 == 0:

          raise ValueError("Division by zero")

        nums.append(num1 // num2)



    while i < len(expr):

      char = expr[i]



        

      if char==' ':

        i += 1

        continue

      if char.isdigit() or char == '.':

        start = i

        while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):

          i += 1

        nums.append(float(expr[start:i]))

        continue

      elif char == '(':

        end = find_closing_parenthesis(expr, i)

        nums.append(evaluate_expression(expr[i + 1:end]))

        i = end

      elif char in '+-':

        while ops and ops[-1] in "*/":

          compute()

        ops.append(char)

      elif char in "*/":

        while ops and ops[-1] in "*/":

          compute()

        ops.append(char)

      i += 1



    while ops:

      compute()

    return nums[0] if nums else 0



  if expression.isdigit() or (expression.startswith("-") and expression[1:].replace(".", "", 1).isdigit()):

    return float(expression)



  return evaluate_expression(expression)


def main():
    test_expressions = [
        "3+5a",                  # Simple addition
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
