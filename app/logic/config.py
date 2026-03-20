from pathlib import Path


# Project paths
BASE_DIR   = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "mood_classifier.pkl"
DATA_PATH  = BASE_DIR / "data" / "processed" / "spotify_tracks_mood_clean.csv"

# Model features
FEATURES: list[str] = [
    "valence",
    "energy",
    "danceability",
    "tempo",
    "acousticness",
    "instrumentalness",
    "loudness",
    "popularity",
]
