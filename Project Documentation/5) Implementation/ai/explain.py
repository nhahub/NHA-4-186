import joblib
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from ai.preprocessing import preprocess_single, feature_names as FEATURE_NAMES

MODEL_DIR = Path(__file__).parent / "model"
model = joblib.load(MODEL_DIR / "xgboost_rul_model.pkl")


class Explainability:

    def __init__(self):
        self.explainer = shap.TreeExplainer(model)

    def explain_single(self, sensor_data: dict) -> dict:
        scaled = preprocess_single(sensor_data)
        shap_values = self.explainer(scaled)

        return {
            "shap_values": shap_values,
            "values": shap_values.values[0].tolist(),
            "base_value": float(shap_values.base_values[0]),
            "data": scaled[0].tolist(),
            "feature_names": list(FEATURE_NAMES),
        }