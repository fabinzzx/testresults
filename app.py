from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    # Reload JSON data every time
    with open("data.json", "r") as file:
        results = json.load(file)

    if request.method == "POST":
        name = request.form.get("name", "").strip().lower()
        if name in results:
            student_data = results[name]
            total = sum(v for k, v in student_data.items() if isinstance(v, int))
            result = {
                "name": name.title(),
                "categories": student_data,
                "total": total
            }
        else:
            result = "Name not found. Please check spelling or contact your instructor."

    return render_template("index.html", result=result)
