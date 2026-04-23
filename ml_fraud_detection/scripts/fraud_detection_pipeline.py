# scripts/fraud_detection_pipeline.py
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import logging
from datetime import datetime

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "job_postings.db"
LOG_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
LOG_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=LOG_DIR / f"ml_fraud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Starting Fraudulent Job Detection Pipeline ===")

def load_data():
    """Load cleaned data from ETL pipeline"""
    try:
        if not DB_PATH.exists():
            raise FileNotFoundError(f"Database not found at {DB_PATH}. Make sure job_postings.db is in the data folder.")
        
        engine = create_engine(f"sqlite:///{DB_PATH}")
        df = pd.read_sql("SELECT * FROM job_postings", engine)
        
        logging.info(f"Loaded {len(df):,} rows from database")
        print(f"✅ Successfully loaded {len(df):,} job postings from the ETL pipeline")
        return df
    except Exception as e:
        logging.error(f"Data loading failed: {e}")
        print(f"❌ Error loading data: {e}")
        raise

if __name__ == "__main__":
    df = load_data()
    
    print("\n📋 Dataset Info:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    print("\n🔍 Fraud Statistics:")
    fraud_count = df['fraudulent'].sum()
    total = len(df)
    print(f"Total jobs          : {total:,}")
    print(f"Fraudulent jobs     : {fraud_count:,} ({fraud_count/total*100:.2f}%)")
    print(f"Real jobs           : {total - fraud_count:,}")
    
    print("\nClass Distribution:")
    print(df['fraudulent'].value_counts())
    
    print("\n✅ Data loaded successfully! Ready for EDA and modeling.")