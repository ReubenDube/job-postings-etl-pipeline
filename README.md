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




