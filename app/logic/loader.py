import logging
from functools import lru_cache

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from app.logic.config import MODEL_PATH, DATA_PATH

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_pipeline() -> Pipeline:
    """Load and cache the trained mood classification pipeline."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")

    logger.info("Loading model from %s", MODEL_PATH)
    pipeline = joblib.load(MODEL_PATH)
    return pipeline


@lru_cache(maxsize=1)
def get_tracks() -> pd.DataFrame:
    """Load and cache the processed tracks' dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

    logger.info("Loading dataset from %s", DATA_PATH)
    df_tracks = pd.read_csv(DATA_PATH)
    return df_tracks
