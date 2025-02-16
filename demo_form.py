'''
demo of form handling in flask
url  with get/post method
'''

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/form", methods=["GET", "POST"])
def form_handler():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        return jsonify({"message": f"Form submitted successfully", "name": name, "age": age})
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)