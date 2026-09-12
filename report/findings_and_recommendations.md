# 🧹 Data Cleaning & Quality Audit — Findings & Technical Summary

**Domain:** Data Analytics  
**Organization:** Oasis Infobyte (OIBSIP)  
**Project:** Level 1 • Task 3  
**Author:** Narendra  

---

## 🔍 Data Quality Audit Findings

### 1. Initial State of Raw Data
- **Duplicates**: 65 redundant duplicate rows detected.
- **Null Incompleteness**: 363 total missing data points across 8 attributes (~4.2% missingness).
- **String Discrepancies**: Inconsistent categorical casings (`M`, `male`, `MALE`, `female`, `F`, `mktg`, `HR`, `Ops`).
- **Currency Encoding**: Financial fields embedded non-numeric characters (`$`, `,`, `USD`).
- **Outliers**: Found biological age anomalies (<18 and >80) and extreme salary entry spikes ($9,999,999).

---

## 🛠 Transformation Steps & Results

1. **Deduplication**: 65 duplicate rows removed (reducing row count from 1,265 to 1,200).
2. **Categorical Normalization**: Mapped all gender and department variations to uniform standard titles.
3. **Currency Parsing**: Converted currency strings into numeric `float64` data types.
4. **Datetime Standardization**: Converted all mixed date formats to standard ISO `YYYY-MM-DD`.
5. **IQR Outlier Capping**: Capped 13 extreme income spikes using Interquartile Range boundaries [$0, $129,677].
6. **Imputation**: Filled numeric missing attributes with median and categorical with mode.
7. **Final Validation**: Cleaned dataset exported with 0 missing values and 100% schema compliance.
