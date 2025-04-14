from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Ensuring the data.json file exists
DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"{DATA_FILE} not found. Please ensure the data file is present.")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    # Reload JSON data every time
    with open(DATA_FILE, "r") as file:
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

# The serverless handler for Vercel
def handler(event, context):
    with app.app_context():
        return app.full_dispatch_request()

