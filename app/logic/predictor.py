from app.logic.loader import pipeline, df_tracks, FEATURES

def search_tracks(track_name: str) -> list[dict]:
    matches = df_tracks[df_tracks["track_name"].str.lower() == track_name.lower()]
    if matches.empty:
        raise ValueError(f"Canción '{track_name}' no encontrada en el dataset.")

    return [
        {"index": i, "track_name": row["track_name"], "artists": row["artists"]}
        for i, row in matches.iterrows()
    ]

def predict_by_index(track_index: int) -> dict:
    track = df_tracks.loc[track_index]
    features = track[FEATURES].values.reshape(1, -1)
    mood = pipeline.predict(features)[0]
    return {
        "track_name": track["track_name"],
        "artists":    track["artists"],
        "mood":       mood,
        "features": {
            "valence":      round(track["valence"], 3),
            "energy":       round(track["energy"], 3),
            "danceability": round(track["danceability"], 3),
            "tempo":        round(track["tempo"], 1),
        }
    }
