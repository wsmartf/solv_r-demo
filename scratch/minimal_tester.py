"""
Minimal test helper for Solver sessions that can be copied to any repository.
No external dependencies, no relative imports needed.
"""
import json
from datetime import datetime

class MinimalTester:
    """
    Self-contained test helper for Solver sessions.
    Provides basic testing functionality without external dependencies.
    """
    
    def __init__(self, flask_app=None):
        """Initialize with optional Flask app for API testing"""
        self.app = flask_app
        self.client = flask_app.test_client() if flask_app else None
        self.results = []
    
    def test(self, name, func):
        """Run and record a test"""
        start_time = datetime.now()
        try:
            func()
            success = True
            error = None
        except AssertionError as e:
            success = False
            error = str(e)
        except Exception as e:
            success = False
            error = f"{type(e).__name__}: {str(e)}"
        
        duration = (datetime.now() - start_time).total_seconds()
        
        result = {
            'name': name,
            'success': success,
            'error': error,
            'duration': duration
        }
        self.results.append(result)
        return result
    
    def assert_equal(self, actual, expected, message=None):
        """Assert equality with custom message"""
        if actual != expected:
            raise AssertionError(message or f"Expected {expected}, got {actual}")
    
    def assert_in(self, item, container, message=None):
        """Assert item is in container"""
        if item not in container:
            raise AssertionError(message or f"Expected {item} to be in {container}")
    
    def request(self, method, endpoint, json_data=None, params=None, as_text=False):
        """Make HTTP request to endpoint"""
        if not self.client:
            raise RuntimeError("Flask app not initialized")
        
        if method.upper() == 'GET':
            response = self.client.get(endpoint, query_string=params)
        elif method.upper() == 'POST':
            response = self.client.post(endpoint, json=json_data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if as_text:
            return response.status_code, response.get_data(as_text=True)
        return response.status_code, response.json if response.is_json else response.data
    
    def print_results(self):
        """Print test results"""
        print("\n=== Test Results ===")
        for result in self.results:
            status = "✓" if result['success'] else "✗"
            print(f"\n{status} {result['name']} ({result['duration']:.3f}s)")
            if not result['success']:
                print(f"  Error: {result['error']}")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        print(f"\nTotal: {total}, Passed: {passed}, Failed: {total - passed}")

# Example usage
if __name__ == "__main__":
    # Example without Flask
    tester = MinimalTester()
    
    def test_basic_math():
        tester.assert_equal(2 + 2, 4, "Basic addition failed")
        tester.assert_in(3, [1, 2, 3], "List membership failed")
    
    tester.test("Basic Math", test_basic_math)
    tester.print_results()
