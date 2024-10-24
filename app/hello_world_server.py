from flask import Flask, request, jsonify
from calculator import calculate, evaluate_equation
from greeting import create_greeting
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/greet")
def greet():
    name = request.args.get('name')
    return create_greeting(name)

@app.route("/calculate", methods=['POST'])
def calculator():
    """
    Calculator endpoint that accepts either:
    1. JSON in the format:
       {
           "operation": "add|subtract|multiply|divide",
           "numbers": [n1, n2, ...]
       }
    2. JSON with equation string:
       {
           "equation": "10*4+3-2"
       }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if "equation" in data:
            result = evaluate_equation(data["equation"])
        else:
            result = calculate(data)
            
        return jsonify({"result": result})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run()
