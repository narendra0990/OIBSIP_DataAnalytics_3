# 🧹 Systematic Data Cleaning & Quality Audit Pipeline

**Organization:** Oasis Infobyte (OIBSIP)  
**Track:** Data Analytics (Level 1 • Task 3)  
**Author:** Narendra

---

## 📌 Project Overview
This project builds a systematic data cleaning and transformation pipeline that converts an uncurated dirty dataset into a production-ready asset. It handles duplicate removal, categorical harmonization, mixed-date parsing, currency symbol extraction, IQR outlier treatment, and statistical imputations.

---

## 📁 Repository Structure
```text
├── data/
│   ├── raw_dirty_dataset.csv
│   └── cleaned_dataset.csv
├── notebooks/
│   └── data_cleaning_pipeline.ipynb
├── run_cleaning.py
├── requirements.txt
└── README.md
```

---

## 📊 Before vs. After Quality Summary
- **Duplicates**: 65 duplicate records detected and purged.
- **Null Values**: Total missing values reduced from 363 to 0 via median & mode imputation.
- **Outliers**: Extreme income anomalies capped using Interquartile Range (IQR) boundaries.
- **Schema**: Enforced strict data types across datetime, numeric floats, and categorical attributes.

---

## 🚀 How to Run Locally
```bash
pip install -r requirements.txt
python run_cleaning.py
jupyter notebook notebooks/data_cleaning_pipeline.ipynb
```
