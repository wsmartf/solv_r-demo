"""
Universal template for Solver sessions.
Can be used with any repository, with or without Flask.
"""


class TestSession:
    """
    Template for testing in Solver sessions.
    Copy MinimalTester and this template to start testing in any repository.
    """

    def __init__(self):
        """
        Initialize test session.
        Import your modules here using try/except to handle missing dependencies.
        """
        import os
        import sys

        # Add project root to Python path if needed
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if project_root not in sys.path:
            sys.path.append(project_root)

        # Import the minimal tester from the same directory
        from minimal_tester import MinimalTester

        # Try to import Flask app if it exists
        try:
            from app.calculator_server import app
            self.tester = MinimalTester(flask_app=app)
            self.has_flask = True
            print("Flask app found and initialized")
        except ImportError as e:
            self.tester = MinimalTester()
            self.has_flask = False
            print(f"Note: Flask app not available ({str(e)})")

    def test_direct_functions(self):
        """
        Test functions directly.
        Add your function tests here.
        """

        def run_tests():
            # Example: Testing a calculator function
            try:
                from app.calculator import calculate
                result = calculate({"operation": "add", "numbers": [1, 2]})
                self.tester.assert_equal(result, 3, "Calculator addition failed")
            except ImportError:
                print("Note: Calculator module not found, skipping those tests")

            # Add more direct function tests here
            # Example:
            x = 10 + 20
            self.tester.assert_equal(x, 30, "Basic math failed")

        self.tester.test("Direct Function Tests", run_tests)

    def test_api_endpoints(self):
        """
        Test API endpoints if Flask app is available.
        Add your API tests here.
        """
        if not self.has_flask:
            print("Note: Flask app not available, skipping API tests")
            return

        def test_endpoints():
            # Test GET endpoint
            status, data = self.tester.request('GET', '/hello', as_text=True)
            self.tester.assert_equal(status, 200)
            self.tester.assert_equal(data, "Hello, World!")

            # Test POST endpoint with JSON
            status, data = self.tester.request(
                'POST',
                '/calculate',
                json_data={"equation": "10*4+3-2"}
            )
            self.tester.assert_equal(status, 200)
            self.tester.assert_equal(data.get('result'), 41)

        self.tester.test("API Endpoints", test_endpoints)


def main():
    """
    Main entry point for testing.
    Shows test results and handles errors.
    """
    try:
        session = TestSession()

        print("=== Running Tests ===")
        session.test_direct_functions()
        session.test_api_endpoints()

        session.tester.print_results()

    except Exception as e:
        print(f"\nError setting up tests: {type(e).__name__} - {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if required modules are available")
        print("2. Verify file paths and imports")
        print("3. Ensure minimal_tester.py is in the same directory")


if __name__ == "__main__":
    main()