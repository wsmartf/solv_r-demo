import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from universal_template import TestSession

class CalculatorTestSession(TestSession):
    def test_direct_functions(self):
        def run_tests():
            from app.calculator import calculate, evaluate_equation
            
            # Test basic arithmetic operations
            self.tester.assert_equal(evaluate_equation("2+2"), 4, "Simple addition failed")
            self.tester.assert_equal(evaluate_equation("10-3"), 7, "Simple subtraction failed")
            self.tester.assert_equal(evaluate_equation("4*5"), 20, "Simple multiplication failed")
            self.tester.assert_equal(evaluate_equation("15/3"), 5, "Simple division failed")
            
            # Test operator precedence
            self.tester.assert_equal(evaluate_equation("2+3*4"), 14, "Operator precedence failed")
            self.tester.assert_equal(evaluate_equation("10/2+3"), 8, "Division precedence failed")
            
            # Test dictionary-based calculations
            tests = [
                ({"operation": "add", "numbers": [1, 2, 3]}, 6),
                ({"operation": "multiply", "numbers": [2, 3, 4]}, 24),
                ({"operation": "subtract", "numbers": [10, 3, 2]}, 5),
                ({"operation": "divide", "numbers": [20, 2, 2]}, 5),
            ]
            for input_data, expected in tests:
                self.tester.assert_equal(calculate(input_data), expected, f"Operation {input_data['operation']} failed")

        self.tester.test("Direct Calculator Tests", run_tests)

    def test_api_endpoints(self):
        if not self.has_flask:
            print("Note: Flask app not available, skipping API tests")
            return

        def test_endpoints():
            # Test equation-based calculations
            equations = [
                ("2+2", 4),
                ("10*4+3-2", 41),
                ("5*5/5+5", 10),  # (5*5)/5 + 5 = 25/5 + 5 = 5 + 5 = 10
                ("2+3*4", 14),    # 2 + (3*4) = 2 + 12 = 14
            ]
            for equation, expected in equations:
                status, data = self.tester.request('POST', '/calculate', 
                    json_data={"equation": equation})
                self.tester.assert_equal(status, 200, f"Equation {equation} failed with status {status}")
                self.tester.assert_equal(data.get('result'), expected, f"Equation {equation} gave wrong result")

            # Test operation-based calculations
            # Test valid operations
            operations = [
                ({"operation": "add", "numbers": [5, 3, 2]}, 10),
                ({"operation": "multiply", "numbers": [2, 4, 3]}, 24),
                ({"operation": "subtract", "numbers": [10, 3]}, 7),
                ({"operation": "divide", "numbers": [20, 4]}, 5),
            ]
            
            # Test error cases
            # Test UI elements
            status, html = self.tester.request('GET', '/', as_text=True)
            self.tester.assert_equal(status, 200, "Failed to load calculator UI")
            
            # Verify essential UI elements
            required_elements = [
                'Simple Calculator',
                'id="equation"',
                'id="result"',
                'id="history-list"',
                'class="history"',
                'function calculate()',
                'addToHistory('
            ]
            for element in required_elements:
                self.tester.assert_in(element, html, f"Missing UI element: {element}")

            # Test error cases
            error_cases = [
                ({"equation": "2++2"}, 400),  # Invalid operator
                ({"equation": "2/0"}, 400),   # Division by zero
                ({"operation": "invalid", "numbers": [1, 2]}, 400),  # Invalid operation
                ({"operation": "add"}, 400),  # Missing numbers
                ({}, 400),  # Empty input
            ]
            
            for input_data, expected in operations:
                status, data = self.tester.request('POST', '/calculate', 
                    json_data=input_data)
                self.tester.assert_equal(status, 200, f"Operation {input_data['operation']} failed with status {status}")
                self.tester.assert_equal(data.get('result'), expected, f"Operation {input_data['operation']} gave wrong result")

            for input_data, expected_status in error_cases:
                status, data = self.tester.request('POST', '/calculate', 
                    json_data=input_data)
                self.tester.assert_equal(status, expected_status, f"Error case {input_data} gave unexpected status")
                self.tester.assert_in('error', data, f"Error case {input_data} missing error message")

        self.tester.test("Calculator API Tests", test_endpoints)

if __name__ == "__main__":
    session = CalculatorTestSession()
    print("=== Running Calculator Tests ===")
    session.test_direct_functions()
    session.test_api_endpoints()
    session.tester.print_results()
