import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from app.greeting import create_greeting
from app.calculator import calculate
from app.hello_world_server import app
class TestRunner:
    """Simple test runner that can be executed with plain Python"""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_test(self, test_func):
        """Run a test function and track its result"""
        self.tests_run += 1
        test_name = test_func.__name__
        print(f"\nRunning test: {test_name}")
        try:
            test_func()
            print(f"✓ {test_name} passed")
            self.tests_passed += 1
        except AssertionError as e:
            print(f"✗ {test_name} failed: {str(e)}")
            self.tests_failed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with error: {str(e)}")
            self.tests_failed += 1
    
    def assert_equal(self, actual, expected, message=None):
        """Custom assertion helper"""
        if actual != expected:
            raise AssertionError(message or f"Expected {expected}, but got {actual}")

def test_greeting_logic():
    """Unit tests for greeting logic"""
    # Test default greeting
    result = create_greeting()
    assert result == "Hello, World!", "Default greeting failed"
    
    # Test custom name
    result = create_greeting("Alice")
    assert result == "Hello, Alice!", "Custom greeting failed"
    
    # Test empty name
    result = create_greeting("")
    assert result == "Hello, !", "Empty name greeting failed"
    
    # Test None name
    result = create_greeting(None)
    assert result == "Hello, World!", "None name greeting failed"

def test_flask_endpoints():
    """Integration tests for Flask endpoints"""
    client = app.test_client()
    
    # Test root endpoint
    response = client.get('/')
    assert response.status_code == 200, "Root endpoint status code failed"
    assert response.data.decode('utf-8') == "Hello, World!", "Root endpoint response failed"
    
    # Test greet endpoint default
    response = client.get('/greet')
    assert response.status_code == 200, "Greet endpoint default status code failed"
    assert response.data.decode('utf-8') == "Hello, World!", "Greet endpoint default response failed"
    
    # Test greet endpoint with name
    response = client.get('/greet?name=Alice')
    assert response.status_code == 200, "Greet endpoint with name status code failed"
    assert response.data.decode('utf-8') == "Hello, Alice!", "Greet endpoint with name response failed"
    
    # Test non-existent endpoint
    response = client.get('/nonexistent')
    assert response.status_code == 404, "Non-existent endpoint status code failed"

def test_calculator_logic():
    """Unit tests for calculator logic"""
    # Test addition
    result = calculate({"operation": "add", "numbers": [5, 3, 2]})
    assert result == 10, "Addition failed"
    
    # Test subtraction
    result = calculate({"operation": "subtract", "numbers": [10, 3, 2]})
    assert result == 5, "Subtraction failed"
    
    # Test multiplication
    result = calculate({"operation": "multiply", "numbers": [4, 3, 2]})
    assert result == 24, "Multiplication failed"
    
    # Test division
    result = calculate({"operation": "divide", "numbers": [24, 2, 3]})
    assert result == 4, "Division failed"
    
    # Test error handling
    try:
        calculate({"operation": "divide", "numbers": [10, 0]})
        assert False, "Should have raised division by zero error"
    except ValueError as e:
        assert str(e) == "Division by zero", "Wrong error message"

def test_calculator_endpoint():
    """Integration tests for calculator endpoint"""
    client = app.test_client()
    
    # Test successful calculation
    data = {
        "operation": "add",
        "numbers": [5, 3, 2]
    }
    response = client.post('/calculate', 
                         json=data,
                         content_type='application/json')
    assert response.status_code == 200, "Calculator endpoint status code failed"
    result = json.loads(response.data.decode('utf-8'))
    assert result["result"] == 10, "Calculator endpoint addition failed"
    
    # Test invalid operation
    data = {
        "operation": "invalid",
        "numbers": [5, 3]
    }
    response = client.post('/calculate', 
                         json=data,
                         content_type='application/json')
    assert response.status_code == 400, "Invalid operation should return 400"
    
    # Test missing data
    response = client.post('/calculate', 
                         json={},
                         content_type='application/json')
    assert response.status_code == 400, "Missing data should return 400"
    
    # Test division by zero
    data = {
        "operation": "divide",
        "numbers": [10, 0]
    }
    response = client.post('/calculate', 
                         json=data,
                         content_type='application/json')
    assert response.status_code == 400, "Division by zero should return 400"

if __name__ == '__main__':
    # Create and run test suite
    runner = TestRunner()
    
    print("=== Running Greeting Logic Tests ===")
    runner.run_test(test_greeting_logic)
    
    print("\n=== Running Calculator Logic Tests ===")
    runner.run_test(test_calculator_logic)
    
    print("\n=== Running Flask Endpoint Tests ===")
    runner.run_test(test_flask_endpoints)
    
    print("\n=== Running Calculator Endpoint Tests ===")
    runner.run_test(test_calculator_endpoint)
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Tests run: {runner.tests_run}")
    print(f"Tests passed: {runner.tests_passed}")
    print(f"Tests failed: {runner.tests_failed}")
    
    # Exit with appropriate status code
    sys.exit(1 if runner.tests_failed > 0 else 0)
