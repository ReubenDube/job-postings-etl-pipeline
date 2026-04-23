# Fraudulent Job Detection - Machine Learning Model

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-7B4DFF?style=for-the-badge&logo=xgboost&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

**End-to-end Machine Learning project** to detect fraudulent job postings using the cleaned data from my ETL pipeline.

##  Project Overview
Built a classification model to predict whether a job posting is fraudulent or legitimate. 
Achieved **ROC-AUC of 0.9510** and **72% recall** on fraudulent jobs.

##  Technologies Used
- Python, Pandas, Scikit-learn
- XGBoost (Best performing model)
- SQLAlchemy (loading data from ETL)
- Joblib (model persistence)
- Matplotlib & Seaborn (visualization)

##  Key Results
- **ROC-AUC Score**: 0.9510
- **Fraud Recall**: 0.72 (catches 72% of fraudulent jobs)
- **Fraud Precision**: 0.66
- Trained on 17,880 job postings (4.84% fraud rate)

##  How to Run

```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the improved model
cd scripts
python improved_model_training.py

```


Skills Demonstrated

End-to-end ML pipeline (EDA → Feature Engineering → Modeling → Evaluation)
Handling class imbalance in fraud detection
Feature engineering and importance analysis
Model training with XGBoost
Reusing data from previous ETL project

🔗 Connection to Project 1
This project builds directly on the Job Postings ETL Pipeline — demonstrating a full data-to-model workflow.
🔮 Future Improvements

Text-based features using TF-IDF or embeddings (description, title)
Hyperparameter tuning with Optuna
Deployment as a web app (Streamlit predictor)
API integration with Job Portal


Made as part of my Data Scientist / ML Engineer portfolio