from flask import Flask, render_template, request
from app.logic.predictor import predict_mood

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error  = None

    if request.method == "POST":
        track_name = request.form.get("track_name", "").strip()
        try:
            result = predict_mood(track_name)
        except ValueError as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
