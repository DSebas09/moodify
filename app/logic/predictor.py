# app/logic/predictor.py
from __future__ import annotations

from typing import Any

import pandas as pd

from app.logic.config import FEATURES, SEARCH_COLUMNS
from app.logic.loader import get_pipeline, get_tracks


def search_tracks(query: str, limit: int | None = None) -> list[dict[str, Any]]:
    """
    Search tracks by name using a case-insensitive partial match.

    Args:
        query: Search string for the track name.
        limit: Optional maximum number of results.

    Returns:
        List of dictionaries with basic track information.

    Raises:
        ValueError: If no tracks match the query.
    """
    df = get_tracks()

    if not query:
        raise ValueError("Search query must not be empty.")

    mask = df["track_name"].str.contains(query, case=False, na=False)
    matches = df[mask]

    if matches.empty:
        raise ValueError(f"No tracks found for: '{query}'")

    if limit is not None:
        matches = matches.head(limit)

    columns = [col for col in SEARCH_COLUMNS if col in matches.columns]
    return matches[columns].to_dict(orient="records")


def get_track_by_id(track_id: str) -> pd.Series:
    """
    Retrieve a single track by its track_id.

    Args:
        track_id: Unique track identifier.

    Returns:
        A pandas Series representing the track.

    Raises:
        ValueError: If the track_id is not found.
    """
    df = get_tracks()
    match = df[df["track_id"] == track_id]

    if match.empty:
        raise ValueError(f"Track with id '{track_id}' was not found.")

    return match.iloc[0]


def predict_mood(track_id: str) -> dict[str, Any]:
    """
    Predict mood for a given track_id.

    Args:
        track_id: Unique track identifier.

    Returns:
        Dictionary with track metadata, predicted mood and features.
    """
    pipeline = get_pipeline()
    track = get_track_by_id(track_id)

    features_vector = track[FEATURES].to_frame().T
    mood = pipeline.predict(features_vector)[0]

    result = {
        "track_id": track["track_id"],
        "track_name": track["track_name"],
        "artists": track["artists"],
        "mood": mood,
        "features": {name: float(track[name]) for name in FEATURES},
    }

    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba(features_vector)[0]
        result["probabilities"] = dict(
            zip(pipeline.classes_.tolist(), probabilities.astype(float).tolist())
        )

    return result
