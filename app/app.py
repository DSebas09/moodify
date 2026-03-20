from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from app.logic.config import AUTOCOMPLETE_MAX_RESULTS
from app.logic.predictor import predict_mood, search_tracks

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    options = None

    if request.method == "POST":
        track_id = request.form.get("track_id")
        if track_id:
            try:
                result = predict_mood(track_id)
            except ValueError as exc:
                error = str(exc)

        else:
            track_name = request.form.get("track_name", "").strip()
            if not track_name:
                error = "Please enter a track name."
            else:
                try:
                    matches = search_tracks(
                        query=track_name,
                        limit=AUTOCOMPLETE_MAX_RESULTS,
                    )
                    if len(matches) == 1:
                        result = predict_mood(matches[0]["track_id"])
                    else:
                        options = matches
                except ValueError as exc:
                    error = str(exc)

    return render_template("index.html", result=result, error=error, options=options)


@app.route("/api/search")
def api_search():
    """
    Lightweight search endpoint for autocomplete.
    Expects a 'q' query string parameter.
    """
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"items": []})

    try:
        matches = search_tracks(query=query, limit=AUTOCOMPLETE_MAX_RESULTS)
    except ValueError:
        return jsonify({"items": []})

    items = [
        {
            "track_id": m["track_id"],
            "track_name": m["track_name"],
            "artists": m.get("artists", ""),
        }
        for m in matches
    ]
    return jsonify({"items": items})


if __name__ == "__main__":
    app.run(debug=True)
