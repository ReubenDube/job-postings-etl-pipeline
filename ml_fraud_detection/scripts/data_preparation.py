# scripts/data_preparation.py
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import logging

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "job_postings.db"
MODELS_DIR = PROJECT_ROOT / "models"

MODELS_DIR.mkdir(exist_ok=True)

def prepare_data():
    """Prepare data for machine learning"""
    print("🔄 Loading and preparing data for modeling...")

    # Load data
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM job_postings", engine)

    # Target variable
    target = 'fraudulent'

    # Select features for modeling
    feature_cols = ['has_salary', 'country', 'industry', 'function', 
                   'employment_type', 'required_experience', 'required_education']

    X = df[feature_cols].copy()
    y = df[target].copy()

    # Handle categorical variables
    categorical_cols = ['country', 'industry', 'function', 'employment_type', 
                       'required_experience', 'required_education']

    label_encoders = {}

    for col in categorical_cols:
        if col in X.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le

    # Save label encoders for later use
    joblib.dump(label_encoders, MODELS_DIR / "label_encoders.joblib")

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"✅ Data prepared successfully!")
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape    : {X_test.shape}")
    print(f"Fraud rate in train: {y_train.mean():.4f}")
    print(f"Fraud rate in test : {y_test.mean():.4f}")

    # Save prepared data
    prepared_data = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'feature_cols': feature_cols
    }
    joblib.dump(prepared_data, MODELS_DIR / "prepared_data.joblib")

    return X_train, X_test, y_train, y_test, feature_cols

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, feature_cols = prepare_data()
    print("\n🎯 Data is ready for model training!")