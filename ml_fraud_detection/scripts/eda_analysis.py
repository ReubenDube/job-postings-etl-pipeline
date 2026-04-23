# scripts/eda_analysis.py
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "job_postings.db"

def load_data():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM job_postings", engine)
    return df

df = load_data()

print("=== Exploratory Data Analysis ===")
print(f"Dataset Shape: {df.shape}\n")

# 1. Fraud Rate
fraud_rate = df['fraudulent'].mean() * 100
print(f"Fraud Rate: {fraud_rate:.2f}%")

# 2. Key Comparisons: Fraud vs Real
print("\n=== Features that might indicate fraud ===")

cols_to_check = ['has_salary', 'country', 'industry', 'function', 'employment_type']

for col in cols_to_check:
    if col in df.columns:
        print(f"\n{col.upper()} vs Fraudulent:")
        fraud_by_col = df.groupby(col)['fraudulent'].agg(['count', 'mean']).round(4)
        fraud_by_col['fraud_%'] = fraud_by_col['mean'] * 100
        print(fraud_by_col.sort_values('fraud_%', ascending=False).head(8))

# 3. Salary Information
print("\nHas Salary Information vs Fraud:")
salary_fraud = df.groupby('has_salary')['fraudulent'].mean() * 100
print(salary_fraud)

# Save a simple plot
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='fraudulent')
plt.title('Distribution of Fraudulent vs Real Job Postings')
plt.xlabel('Fraudulent (1 = Yes, 0 = No)')
plt.ylabel('Count')
plt.savefig(PROJECT_ROOT / "fraud_distribution.png")
print("\n✅ Fraud distribution plot saved as 'fraud_distribution.png'")

print("\n✅ EDA completed! Key insights ready for modeling.")