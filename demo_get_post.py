'''
flask http get and post demo
for get:
http://127.0.0.1:5000/get_example?name=John&age=30
for post:
 curl -X POST http://127.0.0.1:5000/post_example \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "age": 25}'
'''
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/get_example", methods=["GET"])
def get_example():
    # Retrieve query parameters
    print("got request")
    name = request.args.get("name", "Guest")
    age = request.args.get("age", "unknown")
    return jsonify({"message": "Hello, "+ name + "!", "age": age})


@app.route("/post_example", methods=["POST"])
def post_example():
    data = request.json  # Parse JSON body
    name = data.get("name", "Guest")
    age = data.get("age", "unknown")
    return jsonify({"message": "Data received for " + name, "age": age})


@app.route("/test", methods=["GET"])
def test_get_post():
    return render_template("demo_get_post.html")

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=18080)
