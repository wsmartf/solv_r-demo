def evaluate_equation(equation_string):
    """
    Evaluates a mathematical equation string like "10*4+3-2"
    Supports: +, -, *, /
    Respects operator precedence (* and / before + and -)
    """
    # Remove all whitespace
    equation = equation_string.replace(" ", "")
    
    # Helper function to get number and next position
    def get_number(pos):
        num = ""
        while pos < len(equation) and (equation[pos].isdigit() or equation[pos] == '.'):
            num += equation[pos]
            pos += 1
        return float(num), pos
    
    # First pass: handle multiplication and division
    numbers = []
    operators = []
    i = 0
    
    # Get first number
    num, i = get_number(i)
    numbers.append(num)
    
    while i < len(equation):
        op = equation[i]
        i += 1
        
        if op not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid operator: {op}")
        
        num, i = get_number(i)
        
        # Handle multiplication and division immediately
        if op in ['*', '/']:
            prev_num = numbers.pop()
            if op == '*':
                numbers.append(prev_num * num)
            else:
                if num == 0:
                    raise ValueError("Division by zero")
                numbers.append(prev_num / num)
        else:
            numbers.append(num)
            operators.append(op)
    
    # Second pass: handle addition and subtraction
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        else:  # op == '-'
            result -= numbers[i + 1]
    
    return result

def calculate(expression):
    """
    Evaluates a mathematical expression provided as a dictionary
    Example input: {"operation": "add", "numbers": [5, 3]}
    Supported operations: add, subtract, multiply, divide
    """
    operation = expression.get('operation')
    numbers = expression.get('numbers', [])
    
    if not operation or not numbers or len(numbers) < 2:
        raise ValueError("Invalid expression: requires operation and at least two numbers")
    
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All values must be numbers")
    
    result = numbers[0]
    
    if operation == "add":
        for num in numbers[1:]:
            result += num
    elif operation == "subtract":
        for num in numbers[1:]:
            result -= num
    elif operation == "multiply":
        for num in numbers[1:]:
            result *= num
    elif operation == "divide":
        for num in numbers[1:]:
            if num == 0:
                raise ValueError("Division by zero")
            result /= num
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return result
