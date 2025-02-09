from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/hello")
def home():
    return render_template("index.html")

@app.route("/homework")
def homework():
    return render_template("homework.html")

if __name__ == "__main__":
    app.run(debug=True)
