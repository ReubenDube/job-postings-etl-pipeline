# scripts/model_training.py
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import seaborn as sns
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

# Load prepared data
data = joblib.load(MODELS_DIR / "prepared_data.joblib")
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
feature_cols = data['feature_cols']

print("🚀 Starting Model Training...\n")

# 1. Random Forest Model
print("Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight='balanced'   # Helps with imbalance
)
rf_model.fit(X_train, y_train)

# 2. XGBoost Model
print("Training XGBoost...")
xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric='auc'
)
xgb_model.fit(X_train, y_train)

# Evaluate both models
def evaluate_model(model, name):
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print(f"\n=== {name} Model Performance ===")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC-AUC Score: {auc:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")
    
    return model, auc

# Evaluate
rf_model, rf_auc = evaluate_model(rf_model, "Random Forest")
xgb_model, xgb_auc = evaluate_model(xgb_model, "XGBoost")

# Save the best model
if rf_auc > xgb_auc:
    best_model = rf_model
    best_name = "RandomForest"
    best_auc = rf_auc
else:
    best_model = xgb_model
    best_name = "XGBoost"
    best_auc = xgb_auc

joblib.dump(best_model, MODELS_DIR / f"best_fraud_model_{best_name}.joblib")
print(f"\n🎉 Best model saved: {best_name} (AUC: {best_auc:.4f})")

print("\n✅ Model training completed!")