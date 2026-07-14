import joblib
import pandas as pd
from pathlib import Path
from ai.preprocessing import preprocess_single, preprocess_batch

MODEL_DIR = Path(__file__).parent / "model"
model = joblib.load(MODEL_DIR / "xgboost_rul_model.pkl")


class Predictor:

    def predict_single(self, sensor_data: dict) -> float:
        scaled = preprocess_single(sensor_data)
        return float(model.predict(scaled)[0])

    def predict_batch(self, df: pd.DataFrame):
        scaled, processed_df = preprocess_batch(df)
        if scaled is None or processed_df is None:
            return None, None
        preds = model.predict(scaled).reshape(-1)
        if "Engine_ID" in processed_df.columns:
            results = pd.DataFrame({
                "Engine_ID": processed_df["Engine_ID"].values,
                "Predicted_RUL": preds
            })
        else:
            results = pd.DataFrame({"Predicted_RUL": preds})
        return preds, results