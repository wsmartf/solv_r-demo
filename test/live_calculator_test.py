import os
import json
import subprocess
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def start_server():
    """Start the Flask server as a subprocess"""
    server_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'solv_r-demo', 'app', 'calculator_server.py'
    )
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    print("Starting Flask server...")
    process = subprocess.Popen(['python', server_file], env=env)
    time.sleep(2)  # Give the server time to start
    return process

def make_calculation(operation=None, numbers=None, equation=None):
    """Make a POST request to the calculator endpoint"""
    url = 'http://localhost:5000'
    
    if equation is not None:
        data = json.dumps({"equation": equation})
    else:
        data = json.dumps({
            "operation": operation,
            "numbers": numbers
        })
    
    data = data.encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    request = Request(url, data=data, headers=headers, method='POST')
    
    try:
        response = urlopen(request)
        return {
            'status': response.status,
            'data': json.loads(response.read().decode('utf-8'))
        }
    except HTTPError as e:
        return {
            'status': e.code,
            'data': json.loads(e.read().decode('utf-8'))
        }

def run_live_tests():
    """Run tests against a live server"""
    server_process = start_server()
    
    try:
        # Test original format
        print("\n=== Testing Original Format ===")
        
        print("\nTest 1: Addition")
        result = make_calculation("add", [5, 3, 2])
        print(f"5 + 3 + 2 = {result['data']['result']}")
        assert result['status'] == 200 and result['data']['result'] == 10
        
        print("\nTest 2: Multiplication")
        result = make_calculation("multiply", [4, 3, 2])
        print(f"4 * 3 * 2 = {result['data']['result']}")
        assert result['status'] == 200 and result['data']['result'] == 24
        
        # Test equation string format
        print("\n=== Testing Equation String Format ===")
        
        print("\nTest 3: Complex equation (10*4+3-2)")
        result = make_calculation(equation="10*4+3-2")
        print(f"10 * 4 + 3 - 2 = {result['data']['result']}")
        assert result['status'] == 200 and result['data']['result'] == 41
        
        print("\nTest 4: Operator precedence (2+3*4)")
        result = make_calculation(equation="2+3*4")
        print(f"2 + 3 * 4 = {result['data']['result']}")
        assert result['status'] == 200 and result['data']['result'] == 14
        
        print("\nTest 5: Division in equation (20/4+3)")
        result = make_calculation(equation="20/4+3")
        print(f"20 / 4 + 3 = {result['data']['result']}")
        assert result['status'] == 200 and result['data']['result'] == 8
        
        # Test error handling
        print("\nTest 6: Division by zero error")
        result = make_calculation(equation="10/0+5")
        print(f"Expected error response: {result['data']['error']}")
        assert result['status'] == 400 and 'error' in result['data']
        
        print("\nAll live tests passed successfully!")
        
    finally:
        print("\nStopping Flask server...")
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    run_live_tests()
