'''
flask http get demo
http://127.0.0.1:5000/get_example?name=John&age=30
'''
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get_example", methods=["GET"])
def get_example():
    # Retrieve query parameters
    name = request.args.get("name", "Guest")
    age = request.args.get("age", "unknown")
    return jsonify({"message": f"Hello, {name}!", "age": age})

if __name__ == "__main__":
    app.run(debug=True)