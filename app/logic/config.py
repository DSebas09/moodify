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

# Mood labels
MOOD_LABELS: list[str] = ["happy", "energetic", "chill", "sad"]

MOOD_DISPLAY: dict[str, str] = {
    "happy":     "Happy",
    "energetic": "Energetic",
    "chill":     "Chill",
    "sad":       "Sad",
}

# Search & autocomplete
SEARCH_COLUMNS: list[str] = ["track_id", "track_name", "artists", "album_name"]

AUTOCOMPLETE_MIN_CHARS: int = 2
AUTOCOMPLETE_MAX_RESULTS: int = 8

# App settings
DEBUG: bool = False
