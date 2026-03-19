from flask import Flask, render_template, request
from app.logic.predictor import predict_by_index, search_tracks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result   = None
    error    = None
    options  = None

    if request.method == "POST":
        track_index = request.form.get("track_index")
        if track_index:
            result = predict_by_index(int(track_index))

        else:
            track_name = request.form.get("track_name", "").strip()
            try:
                matches = search_tracks(track_name)
                if len(matches) == 1:
                    result = predict_by_index(matches[0]["index"])
                else:
                    options = matches
            except ValueError as e:
                error = str(e)

    return render_template("index.html", result=result, error=error, options=options)

if __name__ == "__main__":
    app.run(debug=True)
