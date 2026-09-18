"""
Machine Learning Training Pipeline for Agricultural Crop Yield Prediction
Trains an ensemble Random Forest regression pipeline with Scikit-learn ColumnTransformer.
"""

import os
import sys
import json
from datetime import datetime

# Configure UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def train_crop_yield_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "crop_yield_data.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    print(f"🌾 Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"📊 Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Define Feature Sets
    categorical_features = ["Crop", "State", "Season", "Soil_Type"]
    numerical_features = [
        "Area_Hectares",
        "Rainfall_mm",
        "Temperature_Celsius",
        "Fertilizer_kg_per_ha",
        "Pesticide_kg_per_ha",
    ]
    target = "Yield_tonnes_per_ha"

    X = df[categorical_features + numerical_features]
    y = df[target]

    # Unique values for metadata & UI dropdowns
    metadata_options = {
        "crops": sorted(df["Crop"].unique().tolist()),
        "states": sorted(df["State"].unique().tolist()),
        "seasons": sorted(df["Season"].unique().tolist()),
        "soils": sorted(df["Soil_Type"].unique().tolist()),
    }

    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"🔹 Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    # Construct Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
            ("num", StandardScaler(), numerical_features),
        ]
    )

    # Construct Pipeline
    model = RandomForestRegressor(
        n_estimators=160,
        max_depth=18,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", model)]
    )

    print("⚙️ Fitting Random Forest Pipeline on agricultural training data...")
    pipeline.fit(X_train, y_train)

    # Evaluate Model
    y_pred = pipeline.predict(X_test)

    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mape = float(np.mean(np.abs((y_test - y_pred) / y_test)) * 100)

    print("\n🎯 Model Evaluation Metrics:")
    print(f"   • R² Score (Accuracy):   {r2:.4f} ({r2*100:.2f}%)")
    print(f"   • Mean Absolute Error:    {mae:.4f} tonnes/ha")
    print(f"   • Root Mean Squared Error: {rmse:.4f} tonnes/ha")
    print(f"   • Mean Abs % Error:       {mape:.2f}%")

    # Save trained pipeline
    model_path = os.path.join(models_dir, "crop_yield_model.pkl")
    joblib.dump(pipeline, model_path)
    print(f"💾 Trained model saved to: {model_path}")

    # Save model metadata
    metadata = {
        "model_name": "Agricultural Crop Yield Predictor (Random Forest Ensemble)",
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": len(df),
        "categorical_features": categorical_features,
        "numerical_features": numerical_features,
        "target": target,
        "target_unit": "tonnes/hectare",
        "options": metadata_options,
        "metrics": {
            "r2_score": round(r2, 4),
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
            "mape": round(mape, 2),
        },
    }

    metadata_path = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"📋 Model metadata & options saved to: {metadata_path}")


if __name__ == "__main__":
    train_crop_yield_model()
