import pandas as pd
from ai.preprocessing import feature_names


def validate_single_input(data: dict):

    for feature in feature_names:

        if feature not in data:
            return False, f"Missing feature: {feature}"

        try:
            float(data[feature])
        except:
            return False, f"{feature} must be numeric"

    return True, "Valid input"


def validate_csv(df: pd.DataFrame):

    if df is None or df.empty:
        return False, "Empty file"

    # check missing columns only
    missing = set(feature_names) - set(df.columns)

    if missing:
        return False, f"Missing columns: {list(missing)}"

    return True, "Valid CSV"