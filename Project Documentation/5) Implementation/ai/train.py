import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
import xgboost as xgb
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

MODEL_DIR = Path(__file__).parent / "model"
scaler = joblib.load(MODEL_DIR / "standard_scaler.pkl")
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")


# =============================================
# Data Generation - Simulates C-MAPSS data
# =============================================

def generate_turbofan_data(n_engines=100, max_cycles=300):
    np.random.seed(42)
    records = []
    for engine_id in range(1, n_engines + 1):
        n_cycles = np.random.randint(80, max_cycles)
        start_cycle = np.random.randint(0, max(1, n_cycles - 50))
        degradation_rate = np.random.uniform(0.5, 2.0)
        base_sensor_noise = np.random.uniform(0.3, 1.5)
        for cycle in range(start_cycle, n_cycles):
            progress = cycle / n_cycles
            rul = n_cycles - cycle
            noise = lambda: np.random.normal(0, base_sensor_noise)
            records.append({
                "unit": engine_id,
                "cycle": cycle,
                "op_setting_1": np.random.normal(0, 0.003),
                "op_setting_2": np.random.normal(0, 0.001),
                "sensor_2": 642.7 + noise() * 0.5 + progress * degradation_rate * 1.5,
                "sensor_3": 1590.5 + noise() * 2 - progress * degradation_rate * 8,
                "sensor_4": 1408.9 + noise() * 1.5 + progress * degradation_rate * 4,
                "sensor_6": 21.6 + np.random.normal(0, 0.008),
                "sensor_7": 553.4 + noise() * 1.0 + progress * degradation_rate * 2.5,
                "sensor_8": 2388.1 + np.random.normal(0, 0.15),
                "sensor_9": 9065.4 + noise() * 12 + progress * degradation_rate * 25,
                "sensor_11": 47.5 + noise() * 0.4 - progress * degradation_rate * 1.5,
                "sensor_12": 521.4 + noise() * 0.6 - progress * degradation_rate * 1.2,
                "sensor_13": 2388.1 + np.random.normal(0, 0.15),
                "sensor_14": 8143.9 + noise() * 6 - progress * degradation_rate * 15,
                "sensor_15": 8.44 + np.random.normal(0, 0.03),
                "sensor_17": 393.2 + noise() * 0.6 + progress * degradation_rate * 1.5,
                "sensor_20": 38.8 + np.random.normal(0, 0.12),
                "sensor_21": 23.3 + np.random.normal(0, 0.06) + progress * degradation_rate * 0.25,
                "RUL": max(rul, 0)
            })
    return pd.DataFrame(records)


# =============================================
# Feature Engineering - Same as project
# =============================================

def prepare_features_all_cycles(df):
    df = df.copy()
    DROP_COLS = ["op_setting_3", "sensor_1", "sensor_5", "sensor_10",
                 "sensor_16", "sensor_18", "sensor_19"]
    for col in DROP_COLS:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna()

    rul = df["RUL"].values
    df = df.drop(columns=["unit", "cycle", "RUL"], errors="ignore")
    df = df.reindex(columns=feature_names, fill_value=0)
    scaled = scaler.transform(df)

    return scaled, rul


# =============================================
# Feature Engineering - Single row (for inference)
# =============================================

def prepare_features_last_cycle(df):
    df = df.copy()
    DROP_COLS = ["op_setting_3", "sensor_1", "sensor_5", "sensor_10",
                 "sensor_16", "sensor_18", "sensor_19"]
    for col in DROP_COLS:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    if "unit" in df.columns and "cycle" in df.columns:
        df = df.sort_values(["unit", "cycle"])
        df = df.groupby("unit", as_index=False).last()
        engine_ids = df["unit"].values
        df = df.drop(columns=["unit", "cycle"], errors="ignore")
    else:
        engine_ids = None

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna()

    df = df.reindex(columns=feature_names, fill_value=0)
    scaled = scaler.transform(df)

    return scaled, df, engine_ids


# =============================================
# Plotting Helpers
# =============================================

def plot_rul_distribution(y_true, y_pred, run_name):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(y_true, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    axes[0].set_title('Actual RUL Distribution')
    axes[0].set_xlabel('RUL')
    axes[0].set_ylabel('Count')
    axes[1].hist(y_pred, bins=30, alpha=0.7, color='coral', edgecolor='black')
    axes[1].set_title('Predicted RUL Distribution')
    axes[1].set_xlabel('RUL')
    axes[1].set_ylabel('Count')
    plt.suptitle(f'RUL Distributions - {run_name}', fontsize=14)
    plt.tight_layout()
    return fig


def plot_prediction_vs_actual(y_true, y_pred, run_name):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_true, y_pred, alpha=0.5, s=20, color='steelblue')
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    ax.set_xlabel('Actual RUL')
    ax.set_ylabel('Predicted RUL')
    ax.set_title(f'Prediction vs Actual - {run_name}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_feature_importance(model, feature_names_list, run_name):
    importance = model.feature_importances_
    indices = np.argsort(importance)[-15:]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(len(indices)), importance[indices], color='steelblue')
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names_list[i] for i in indices])
    ax.set_xlabel('Feature Importance')
    ax.set_title(f'Top 15 Features - {run_name}')
    plt.tight_layout()
    return fig


def plot_residuals(y_true, y_pred, run_name):
    residuals = y_true - y_pred
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(y_pred, residuals, alpha=0.5, s=20, color='steelblue')
    ax.axhline(y=0, color='red', linestyle='--', lw=2)
    ax.set_xlabel('Predicted RUL')
    ax.set_ylabel('Residual (Actual - Predicted)')
    ax.set_title(f'Residual Plot - {run_name}')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_health_distribution(y_pred, run_name):
    critical = int(np.sum(y_pred < 30))
    warning = int(np.sum((y_pred >= 30) & (y_pred < 75)))
    healthy = int(np.sum(y_pred >= 75))
    fig, ax = plt.subplots(figsize=(8, 5))
    categories = ['Critical\n(<30)', 'Warning\n(30-75)', 'Healthy\n(>75)']
    counts = [critical, warning, healthy]
    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    bars = ax.bar(categories, counts, color=colors, edgecolor='black')
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel('Number of Engines')
    ax.set_title(f'Engine Health Distribution - {run_name}')
    plt.tight_layout()
    return fig


# =============================================
# Training Function
# =============================================

def train_model(X_train, y_train, X_test, y_test,
                run_name, n_estimators, max_depth, learning_rate,
                subsample=1.0, colsample_bytree=1.0):

    mlflow.set_experiment("Predictive Maintenance - RUL")
    with mlflow.start_run(run_name=run_name) as run:

        mlflow.set_tag("model_type", "XGBRegressor")
        mlflow.set_tag("task", "RUL_Prediction")
        mlflow.set_tag("dataset", "C-MAPSS_Synthetic")

        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "objective": "reg:squarederror",
            "random_state": 42
        }
        mlflow.log_params(params)

        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

        y_pred = model.predict(X_test)

        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))
        mape = float(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mape", mape)

        mlflow.xgboost.log_model(model, "model")

        fig1 = plot_rul_distribution(y_test, y_pred, run_name)
        mlflow.log_figure(fig1, "plots/rul_distribution.png")
        plt.close(fig1)

        fig2 = plot_prediction_vs_actual(y_test, y_pred, run_name)
        mlflow.log_figure(fig2, "plots/prediction_vs_actual.png")
        plt.close(fig2)

        fig3 = plot_feature_importance(model, list(feature_names), run_name)
        mlflow.log_figure(fig3, "plots/feature_importance.png")
        plt.close(fig3)

        fig4 = plot_residuals(y_test, y_pred, run_name)
        mlflow.log_figure(fig4, "plots/residuals.png")
        plt.close(fig4)

        fig5 = plot_health_distribution(y_pred, run_name)
        mlflow.log_figure(fig5, "plots/health_distribution.png")
        plt.close(fig5)

        summary = pd.DataFrame({
            "Engine_ID": range(1, len(y_pred) + 1),
            "Actual_RUL": y_test,
            "Predicted_RUL": y_pred,
            "Residual": y_test - y_pred
        })
        summary.to_csv("prediction_summary.csv", index=False)
        mlflow.log_artifact("prediction_summary.csv")
        os.remove("prediction_summary.csv")

        print(f"[{run_name}] RMSE: {rmse:.2f} | MAE: {mae:.2f} | R2: {r2:.4f} | MAPE: {mape:.2f}%")

        return rmse, mae, r2


# =============================================
# Main - Run Multiple Experiments
# =============================================

def main(n_estimators, learning_rate, max_depth, subsample, colsample_bytree):

    print("Generating synthetic turbofan data...")
    df = generate_turbofan_data(n_engines=100, max_cycles=300)
    print(f"Generated {len(df)} records for {df['unit'].nunique()} engines")

    X_all, y_all = prepare_features_all_cycles(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42
    )

    print(f"Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"RUL range: {y_all.min():.0f} - {y_all.max():.0f}")

    print("\n--- Experiment 1: Baseline ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name="Baseline - Default Params",
                n_estimators=100, max_depth=6, learning_rate=0.1)

    print("\n--- Experiment 2: Deeper Model ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name="Deeper - More Depth",
                n_estimators=150, max_depth=10, learning_rate=0.1)

    print("\n--- Experiment 3: More Trees ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name="More Trees - n=300",
                n_estimators=300, max_depth=6, learning_rate=0.1)

    print("\n--- Experiment 4: Lower Learning Rate ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name="Low LR - Slower Learning",
                n_estimators=200, max_depth=8, learning_rate=0.05)

    print("\n--- Experiment 5: Subsample + ColSample ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name="Regularized - Subsample",
                n_estimators=200, max_depth=8, learning_rate=0.1,
                subsample=0.8, colsample_bytree=0.8)

    print("\n--- Experiment 6: User Params ---")
    train_model(X_train, y_train, X_test, y_test,
                run_name=f"Custom - n={n_estimators}_d={max_depth}_lr={learning_rate}",
                n_estimators=n_estimators, max_depth=max_depth,
                learning_rate=learning_rate, subsample=subsample,
                colsample_bytree=colsample_bytree)

    print("\nAll experiments complete!")
    print("Run 'mlflow ui' to see results at http://localhost:5000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", "-n", type=int, default=200)
    parser.add_argument("--learning_rate", "-lr", type=float, default=0.1)
    parser.add_argument("--max_depth", "-d", type=int, default=8)
    parser.add_argument("--subsample", "-s", type=float, default=1.0)
    parser.add_argument("--colsample_bytree", "-cs", type=float, default=1.0)
    args = parser.parse_args()

    main(args.n_estimators, args.learning_rate, args.max_depth,
         args.subsample, args.colsample_bytree)
