# scripts/etl_pipeline.py
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
import os
from sqlalchemy import create_engine, text

# ====================== CONFIG ======================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw_job_postings.csv"
DB_PATH = PROJECT_ROOT / "data" / "job_postings.db"
LOG_DIR = PROJECT_ROOT / "logs"

# Create necessary directories
LOG_DIR.mkdir(exist_ok=True)
(PROJECT_ROOT / "data").mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=LOG_DIR / f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Starting Job Postings ETL Pipeline ===")

# ====================== EXTRACT ======================
def extract_data(file_path: Path) -> pd.DataFrame:
    """Extract raw data from CSV"""
    try:
        logging.info(f"Extracting data from {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Successfully extracted {len(df):,} rows and {len(df.columns)} columns")
        print(f"✅ Extract complete! Shape: {df.shape}")
        print("\nFirst 5 rows preview:")
        print(df.head())
        return df
    except Exception as e:
        logging.error(f"Extract failed: {e}")
        print(f"❌ Extract error: {e}")
        raise

# ====================== TRANSFORM ======================
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the raw job postings data"""
    logging.info("Starting data transformation...")
    print("\n🔄 Starting data cleaning and transformation...")

    # Make a copy to avoid modifying original
    df = df.copy()

    # 1. Rename columns to snake_case (standard practice)
    df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

    # 2. Handle missing values
    df['salary_range'] = df['salary_range'].fillna('Not Specified')
    df['location'] = df['location'].fillna('Unknown')
    df['industry'] = df['industry'].fillna('Unknown')
    df['function'] = df['function'].fillna('Unknown')

    # 3. Create new useful features
    df['has_salary'] = df['salary_range'].apply(lambda x: 0 if x == 'Not Specified' else 1)
    
    # Extract country from location (simple heuristic)
    df['country'] = df['location'].apply(lambda x: 
        x.split(',')[0].strip() if isinstance(x, str) and ',' in x else 'Unknown')

    # 4. Clean text columns (basic)
    text_cols = ['title', 'description', 'requirements']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 5. Convert fraudulent column to proper boolean/int
    if 'fraudulent' in df.columns:
        df['fraudulent'] = pd.to_numeric(df['fraudulent'], errors='coerce').fillna(0).astype(int)

    logging.info(f"Transformation complete. Final shape: {df.shape}")
    print(f"✅ Transformation complete! New shape: {df.shape}")
    print("New columns added: has_salary, country")
    
    return df

# ====================== LOAD ======================
def load_data(df: pd.DataFrame, db_path: Path):
    """Load cleaned data into SQLite database"""
    try:
        logging.info(f"Loading data into SQLite database: {db_path}")
        engine = create_engine(f"sqlite:///{db_path}")
        
        # Load the data - this works because pandas handles the SQL generation
        df.to_sql('job_postings', engine, if_exists='replace', index=False)
        
        logging.info("Data successfully loaded into database")
        print("✅ Data successfully loaded into SQLite database!")
        print(f"   Table name: job_postings")
        print(f"   Database file: {db_path.name}")
        
        # --- THE FIX IS HERE ---
        with engine.connect() as conn:
            # Wrap the string in text()
            query = text("SELECT COUNT(*) as count FROM job_postings")
            result = conn.execute(query).fetchone()[0]
            print(f"   Rows in database: {result:,}")
            
    except Exception as e:
        logging.error(f"Load failed: {e}")
        print(f"❌ Load error: {e}")
        raise

# ====================== MAIN PIPELINE ======================
if __name__ == "__main__":
    try:
        # Run the full ETL pipeline
        df_raw = extract_data(DATA_PATH)
        df_clean = transform_data(df_raw)
        load_data(df_clean, DB_PATH)
        
        logging.info("=== ETL Pipeline completed successfully! ===")
        print("\n🎉 Full ETL Pipeline finished successfully!")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")