import joblib
import pandas as pd

MODEL_PATH  = "models/mood_classifier.pkl"
DATA_PATH   = "data/processed/spotify_tracks_mood_clean.csv"

FEATURES = ["valence", "energy", "danceability", "tempo",
            "acousticness", "instrumentalness", "loudness", "popularity"]

pipeline = joblib.load(MODEL_PATH)
df_tracks = pd.read_csv(DATA_PATH)