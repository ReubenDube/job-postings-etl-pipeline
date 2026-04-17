# job-postings-etl-pipeline
End-to-end Python ETL pipeline for job postings data (Data Engineering portfolio project)

# Job Postings ETL Pipeline

**End-to-end data pipeline** built as part of my Data Science / ML Engineer portfolio.

## Overview
This project demonstrates a complete **ETL (Extract, Transform, Load)** pipeline using Python. 
It processes a real-world job postings dataset, cleans it, adds new features, and loads it into a SQLite database.

### Key Features
- Robust file path handling with `pathlib`
- Comprehensive data cleaning and feature engineering
- Logging for monitoring and debugging
- Data loaded into relational database (SQLite)
- Production-ready folder structure

### Technologies Used
- **Python**
- **Pandas** – Data manipulation & cleaning
- **SQLAlchemy** – Database interaction
- **SQLite** – Lightweight relational database
- **Pathlib** – Modern path handling
- **Logging** – Pipeline monitoring

### Pipeline Steps
1. **Extract**: Read raw CSV data (`raw_job_postings.csv`)
2. **Transform**: 
   - Standardize column names
   - Handle missing values
   - Create new features (`has_salary`, `country`)
3. **Load**: Save cleaned data into `job_postings` table in SQLite

### How to Run
```bash
# 1. Clone the repo
git clone https://github.com/yourusername/job-postings-etl-pipeline.git

# 2. Activate virtual environment
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
cd scripts
python etl_pipeline.py
