# Job Postings ETL Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**End-to-end Python ETL pipeline** for real-world job postings data — built as a **Data Engineering** portfolio project.

## 📋 Project Overview
This project demonstrates a complete **Extract, Transform, Load (ETL)** pipeline that processes a dataset of ~17,880 job postings. It cleans messy raw data, engineers new features, and loads everything into a relational database.

**Business Value**: Clean, reliable job data that can be used for analytics, fraud detection, recommendation systems, or powering a job portal.

## 🏗️ Architecture
```mermaid
flowchart LR
    A[Raw CSV\nfake_job_postings.csv] --> B[Extract\nPandas]
    B --> C[Transform\nCleaning + Feature Engineering]
    C --> D[Load\nSQLAlchemy + SQLite]
    D --> E[Interactive Dashboard\nStreamlit]
