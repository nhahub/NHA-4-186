import pandas as pd
import numpy as np
import mlflow

from application.prediction.validator import (
    validate_single_input,
    validate_csv
)

from database.queries import (
    insert_prediction,
    insert_sensor_readings
)

from ai.predict import Predictor
from ai.explain import Explainability


class PredictionService:

    def __init__(self):
      self.predictor = Predictor()
      self.explainer = None
    # ======================================
    # Single Prediction
    # ======================================

    def predict_single(self, sensor_data: dict, user_id: int = None, engine_id: int = 1):

        valid, message = validate_single_input(sensor_data)

        if not valid:
            return {
                "success": False,
                "message": message
            }

        # =========================
        # Model Prediction
        # =========================
        prediction = self.predictor.predict_single(sensor_data)

        status = self.get_health_status(prediction)

        if self.explainer is None:
          self.explainer = Explainability()

        explanation = self.explainer.explain_single(sensor_data)
        # =========================
        # Save to Database
        # =========================
        if user_id is not None:

            prediction_id = insert_prediction(
                user_id=user_id,
                engine_id=engine_id,
                predicted_rul=prediction,
                health_status=status["status"]
            )

            insert_sensor_readings(prediction_id, sensor_data)

        # =========================
        # Return Response
        # =========================
        return {
            "success": True,
            "predicted_rul": prediction,
            "status": status,
            "explanation": explanation
        }

    # ======================================
    # Batch Prediction
    # ======================================

    def predict_batch(
     self,
     df: pd.DataFrame,
      user_id: int = None
     ):

       valid, message = validate_csv(df)

       if not valid:
        return {
            "success": False,
            "message": message
        }

       preds, results = self.predictor.predict_batch(df)
       # Add Health Status
       results["Health_Status"] = results["Predicted_RUL"].apply(
    lambda rul: self.get_health_status(rul)["status"]
)

# Add Recommended Action
       results["Recommended_Action"] = results["Predicted_RUL"].apply(
        lambda rul: self.get_health_status(rul)["action"]
)

# Add Status Icon (اختياري)
       results["Status"] = results["Predicted_RUL"].apply(
         lambda rul: self.get_health_status(rul)["icon"] + " " +
                self.get_health_status(rul)["status"]
)
       if preds is None or len(preds) == 0:
        return {
            "success": False,
            "message": "No valid predictions"
        }

    # ======================================
    # Log Batch Predictions to MLflow
    # ======================================

       try:
         mlflow.set_experiment("Predictive Maintenance - Inference")
         with mlflow.start_run(run_name="batch_prediction"):
           mlflow.log_param("num_engines", len(preds))
           mlflow.log_param("prediction_type", "batch")

           mlflow.log_metric("avg_rul", float(np.mean(preds)))
           mlflow.log_metric("min_rul", float(np.min(preds)))
           mlflow.log_metric("max_rul", float(np.max(preds)))
           mlflow.log_metric("std_rul", float(np.std(preds)))
           mlflow.log_metric("median_rul", float(np.median(preds)))

           critical = int(np.sum(preds < 30))
           warning = int(np.sum((preds >= 30) & (preds < 75)))
           healthy = int(np.sum(preds >= 75))

           mlflow.log_metric("engines_critical", critical)
           mlflow.log_metric("engines_warning", warning)
           mlflow.log_metric("engines_healthy", healthy)

           pred_df = pd.DataFrame({"Predicted_RUL": preds})
           mlflow.log_table(pred_df, "predictions/batch_results.json")
       except Exception:
         pass

    # ======================================
    # Save Predictions to Database
    # ======================================

       if user_id is not None:

        for _, row in results.iterrows():

            status = self.get_health_status(row["Predicted_RUL"])

            insert_prediction(
                user_id=user_id,
                engine_id=int(row["Engine_ID"]),
                predicted_rul=float(row["Predicted_RUL"]),
                health_status=status["status"]
            )

       return {
        "success": True,
        "results": results
    }
    # ======================================
    # Engine Health Status
    # ======================================

    @staticmethod
    def get_health_status(rul):

        if rul > 80:
            return {
                "status": "Healthy",
                "message": "Engine is Healthy",
                "color": "success",
                "icon": "🟢",
                "action": "Continue normal operation."
            }

        elif rul > 30:
            return {
                "status": "Warning",
                "message": "Maintenance Recommended Soon",
                "color": "warning",
                "icon": "🟡",
                "action": "Schedule maintenance inspection."
            }

        else:
            return {
                "status": "Critical",
                "message": "Immediate Maintenance Required",
                "color": "error",
                "icon": "🔴",
                "action": "Stop operation immediately."
            }