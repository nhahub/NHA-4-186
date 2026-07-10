import joblib
import pandas as pd
import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).parent / "model"

scaler = joblib.load(MODEL_DIR / "standard_scaler.pkl")
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")

DROP_COLS = ["op_setting_3", "sensor_1", "sensor_5", "sensor_10",
             "sensor_16", "sensor_18", "sensor_19"]


def preprocess_single(sensor_data: dict) -> np.ndarray:
    df = pd.DataFrame([sensor_data])
    df = df.reindex(columns=feature_names, fill_value=0)
    df = df.fillna(0)
    return scaler.transform(df)


def preprocess_batch(df: pd.DataFrame):
    df = df.copy()
    for col in DROP_COLS:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    engine_ids = None
    if "unit" in df.columns and "cycle" in df.columns:
        df = df.sort_values(["unit", "cycle"])
        df = df.groupby("unit", as_index=False).last()
        engine_ids = df["unit"].values
        df = df.drop(columns=["unit", "cycle"], errors="ignore")
    else:
        df = df.drop(columns=["unit"], errors="ignore")

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna()

    if df.empty:
        return None, None

    df = df.reindex(columns=feature_names, fill_value=0)
    scaled = scaler.transform(df)

    processed_df = pd.DataFrame(scaled, columns=feature_names)
    if engine_ids is not None:
        processed_df.insert(0, "Engine_ID", engine_ids)

    return scaled, processed_df