# scripts/improved_model_training.py
import pandas as pd
import joblib
from pathlib import Path
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt

print("🚀 Starting Improved Fraud Detection Model Training...\n")

# Load data
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "job_postings.db"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")
df = pd.read_sql("SELECT * FROM job_postings", engine)

# Additional feature engineering
df['text_length'] = df['description'].astype(str).str.len()
df['title_length'] = df['title'].astype(str).str.len()
df['has_benefits'] = df['benefits'].notna().astype(int)
df['has_requirements'] = df['requirements'].notna().astype(int)

# Features for modeling
feature_cols = ['has_salary', 'country', 'industry', 'function', 'employment_type',
                'required_experience', 'required_education', 'text_length', 
                'title_length', 'has_benefits', 'has_requirements']

X = df[feature_cols].copy()
y = df['fraudulent'].copy()

# Fill missing values and encode categorical features
categorical_cols = ['country', 'industry', 'function', 'employment_type', 
                   'required_experience', 'required_education']

label_encoders = {}

for col in categorical_cols:
    if col in X.columns:
        # Fill NaN with a special category
        X[col] = X[col].fillna('Unknown').astype(str)
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Calculate class weights for imbalance
scale_pos_weight = (len(y_train) - y_train.sum()) / y_train.sum()

print(f"Using scale_pos_weight = {scale_pos_weight:.2f} to handle imbalance")

# Train Improved XGBoost with class weights
print("Training Improved XGBoost with class weighting...")
xgb_model = XGBClassifier(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric='auc'
)

xgb_model.fit(X_train, y_train)

# Evaluate
y_pred = xgb_model.predict(X_test)
y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]

print("\n=== Improved XGBoost Model Performance ===")
print(classification_report(y_test, y_pred))
auc = roc_auc_score(y_test, y_pred_proba)
print(f"ROC-AUC Score: {auc:.4f}")

cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{cm}")

# Feature Importance
plt.figure(figsize=(12, 8))
importance = pd.Series(xgb_model.feature_importances_, index=feature_cols)
importance = importance.sort_values(ascending=True)
importance.plot(kind='barh')
plt.title('Feature Importance - Improved XGBoost Model')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "feature_importance.png")
print("\n✅ Feature importance plot saved!")

# Save model and encoders
joblib.dump(xgb_model, MODELS_DIR / "improved_xgboost_fraud_model.joblib")
joblib.dump(label_encoders, MODELS_DIR / "label_encoders.joblib")

print(f"\n🎉 Improved model saved successfully! (AUC: {auc:.4f})")
print("✅ Improved model training completed!")