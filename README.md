# Job Postings ETL Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**End-to-end Python ETL pipeline** for real-world job postings data — built as a **Data Engineering / Data Science** portfolio project.

## 📋 Project Overview
This project demonstrates a complete **Extract, Transform, Load (ETL)** pipeline that processes a dataset of **17,880 job postings**. 

It takes messy raw data from a CSV file, cleans it, engineers useful features, and loads the cleaned data into a SQLite database. The pipeline is production-ready with proper logging and robust path handling.

**Business Value**: Produces clean, reliable job data that can power analytics, fraud detection models, job recommendation systems, or enhance a job portal website.

## 🏗️ Architecture
```mermaid
flowchart LR
    A[Raw CSV<br>raw_job_postings.csv] --> B[Extract<br>Pandas]
    B --> C[Transform<br>Cleaning + Feature Engineering]
    C --> D[Load<br>SQLAlchemy + SQLite]
    D --> E[Interactive Dashboard<br>Streamlit]
✨ Key Features

Robust file handling using pathlib
Comprehensive data cleaning and transformation
New feature engineering (has_salary, country)
Detailed logging for monitoring and debugging
Data persisted in a relational SQLite database
Interactive Streamlit dashboard for data exploration

 **TECHNOLOGIES USED**

Python — Core language
Pandas — Data manipulation & cleaning
SQLAlchemy — Database operations
SQLite — Lightweight relational database
Logging — Pipeline observability
Streamlit — Interactive dashboard

**PIPELINE RESULTS**

Raw Data: 17,880 rows × 18 columns
Cleaned Data: 17,880 rows × 20 columns
New columns created: has_salary, country

**HOW TO RUN**
Bash# 1. Clone the repository
git clone https://github.com/ReubenDube/job-postings-etl-pipeline.git
cd job-postings-etl-pipeline

# 2. Activate virtual environment (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the ETL pipeline
cd scripts
python etl_pipeline.py

# 5. (Optional) Launch interactive dashboard
cd ..
streamlit run dashboard.py


**PROJECT STRUCTURE**
textjob-postings-etl-pipeline/
├── data/                    # Contains raw_job_postings.csv and job_postings.db
├── scripts/
│   └── etl_pipeline.py      # Main ETL script
├── logs/                    # Execution log files
├── dashboard.py             # Interactive Streamlit dashboard
├── requirements.txt
├── .gitignore
└── README.md

**SKILLS DEMOSTRATED**

Designing and implementing end-to-end ETL pipelines
Data cleaning and feature engineering at scale
Working with relational databases (SQLite)
Writing clean, maintainable, and well-logged Python code
Creating interactive data dashboards
Professional project organization and documentation

 **FUTURE ENHANCEMENT (Planned)**

Scheduling the pipeline (APScheduler / Prefect)
Cloud deployment (AWS S3 + RDS or Azure)
Integration with my existing Job Portal website
Building a Fraudulent Job Prediction ML model (Project 2)


