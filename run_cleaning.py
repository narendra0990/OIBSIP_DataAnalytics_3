import os
import pandas as pd
import numpy as np

def clean_data_pipeline():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, "data", "raw_dirty_dataset.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned_dataset.csv")
    
    print("=" * 85)
    print("       OASIS INFOBYTE: DATA ANALYTICS INTERNSHIP (LEVEL 1 - TASK 3)       ")
    print("                 SYSTEMATIC DATA CLEANING & QUALITY AUDIT                 ")
    print("=" * 85)
    
    # 1. Load Raw Dataset & Initial Data Quality Report
    df_raw = pd.read_csv(raw_path)
    initial_rows = len(df_raw)
    initial_duplicates = df_raw.duplicated().sum()
    initial_nulls = df_raw.isnull().sum().to_dict()
    initial_dtypes = df_raw.dtypes.to_dict()
    
    print("\n--- 1. INITIAL DATA QUALITY AUDIT REPORT ---")
    print(f"Total Rows: {initial_rows}, Total Columns: {df_raw.shape[1]}")
    print(f"Duplicate Rows Detected: {initial_duplicates}")
    print("\nMissing Values per Attribute:")
    for col, null_count in initial_nulls.items():
        print(f"  * {col:18}: {null_count:4d} missing ({null_count/initial_rows*100:5.2f}%)")
    print("\nInitial Column Data Types:")
    for col, dtype in initial_dtypes.items():
        print(f"  * {col:18}: {str(dtype)}")
        
    # Begin Transformations on working copy
    df = df_raw.copy()
    
    # Step 1: Duplicate Removal
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after_dedup = len(df)
    dedup_removed = initial_rows - rows_after_dedup
    print(f"\n[Step 1] Removed {dedup_removed} duplicate rows. Remaining: {rows_after_dedup} rows.")
    
    # Step 2: String Trimming & Formatting
    string_cols = ["Customer_ID", "Full_Name", "Gender", "Department"]
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})
        
    df["Customer_ID"] = df["Customer_ID"].str.upper()
    df["Full_Name"] = df["Full_Name"].str.title()
    print("[Step 2] Whitespace trimmed and string casings normalized.")
    
    # Step 3: Categorical Standardization
    gender_map = {
        "MALE": "Male", "Male": "Male", "male": "Male", "M": "Male",
        "FEMALE": "Female", "Female": "Female", "female": "Female", "F": "Female",
        "OTHER": "Other", "Other": "Other", "Unknown": np.nan
    }
    df["Gender"] = df["Gender"].map(gender_map)
    
    dept_map = {
        "Sales": "Sales", "sales": "Sales",
        "Engineering": "Engineering", "ENGINEERING": "Engineering",
        "Marketing": "Marketing", "mktg": "Marketing",
        "Human Resources": "Human Resources", "HR": "Human Resources",
        "Operations": "Operations", "Ops": "Operations"
    }
    df["Department"] = df["Department"].map(dept_map)
    print("[Step 3] Categorical labels standardized for Gender and Department.")
    
    # Step 4: Currency & Numeric String Parsing for Annual_Income
    def parse_currency(val):
        if pd.isna(val):
            return np.nan
        s = str(val).replace("$", "").replace(",", "").replace("USD", "").strip()
        try:
            return float(s)
        except ValueError:
            return np.nan
            
    df["Annual_Income"] = df["Annual_Income"].apply(parse_currency)
    print("[Step 4] Annual_Income parsed from currency strings to numeric float.")
    
    # Step 5: Datetime Standardization
    df["Join_Date"] = pd.to_datetime(df["Join_Date"], format="mixed", errors="coerce")
    print("[Step 5] Join_Date unified to standardized datetime format.")
    
    # Step 6: Outlier Detection & Anomaly Treatment (IQR Method)
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df.loc[(df["Age"] < 18) | (df["Age"] > 80), "Age"] = np.nan
    
    df.loc[df["Annual_Income"] <= 0, "Annual_Income"] = np.nan
    income_valid = df["Annual_Income"].dropna()
    
    q1 = income_valid.quantile(0.25)
    q3 = income_valid.quantile(0.75)
    iqr = q3 - q1
    lower_bound = max(0, q1 - 1.5 * iqr)
    upper_bound = q3 + 1.5 * iqr
    
    income_outliers_count = (df["Annual_Income"] > upper_bound).sum()
    df["Annual_Income"] = df["Annual_Income"].clip(lower=lower_bound, upper=upper_bound)
    print(f"[Step 6] Outliers treated: {income_outliers_count} income spikes capped via IQR bounds [${lower_bound:,.0f}, ${upper_bound:,.0f}].")
    
    df["Performance_Score"] = pd.to_numeric(df["Performance_Score"], errors="coerce")
    df.loc[(df["Performance_Score"] < 1.0) | (df["Performance_Score"] > 5.0), "Performance_Score"] = np.nan
    
    # Step 7: Missing Value Imputation
    missing_id_idx = df[df["Customer_ID"].isna()].index
    for idx in missing_id_idx:
        df.loc[idx, "Customer_ID"] = f"CUST_{2000 + idx}"
        
    df["Full_Name"] = df["Full_Name"].fillna("Unknown Client")
    
    median_age = df["Age"].median()
    df["Age"] = df["Age"].fillna(median_age).round().astype(int)
    
    median_income = df["Annual_Income"].median()
    df["Annual_Income"] = df["Annual_Income"].fillna(median_income).round(2)
    
    median_perf = df["Performance_Score"].median()
    df["Performance_Score"] = df["Performance_Score"].fillna(median_perf).round(1)
    
    mode_gender = df["Gender"].mode()[0]
    df["Gender"] = df["Gender"].fillna(mode_gender)
    
    mode_dept = df["Department"].mode()[0]
    df["Department"] = df["Department"].fillna(mode_dept)
    
    df["Join_Date"] = df["Join_Date"].fillna(df["Join_Date"].median())
    print("[Step 7] Missing values successfully imputed with median (numeric) & mode (categorical).")
    
    # Step 8: Final Dtype Enforcement
    df["Join_Date"] = df["Join_Date"].dt.strftime("%Y-%m-%d")
    
    # Export Cleaned Dataset
    df.to_csv(cleaned_path, index=False)
    print(f"\n[Step 8] Cleaned dataset saved to: {cleaned_path}")
    
    # 2. Before vs. After Data Quality Summary Table
    comparison_data = []
    for col in df_raw.columns:
        raw_nulls = df_raw[col].isnull().sum()
        clean_nulls = df[col].isnull().sum()
        raw_type = str(df_raw[col].dtype)
        clean_type = str(df[col].dtype)
        comparison_data.append({
            "Feature": col,
            "Raw Nulls": raw_nulls,
            "Clean Nulls": clean_nulls,
            "Raw Dtype": raw_type,
            "Clean Dtype": clean_type,
            "Audit Status": "[CLEANSED]" if clean_nulls == 0 else "[CHECK]"
        })
        
    summary_df = pd.DataFrame(comparison_data)
    
    print("\n" + "=" * 85)
    print("                     BEFORE VS. AFTER QUALITY AUDIT SUMMARY                     ")
    print("=" * 85)
    print(f"Original Row Count   : {initial_rows}")
    print(f"Cleaned Row Count    : {len(df)} (Removed {dedup_removed} duplicates)")
    print(f"Original Duplicates  : {initial_duplicates}  ->  Final Duplicates: {df.duplicated().sum()}")
    print(f"Original Total Nulls : {sum(initial_nulls.values())}  ->  Final Total Nulls: {df.isnull().sum().sum()}")
    print("-" * 85)
    print(summary_df.to_string(index=False))
    print("=" * 85)
    print("Data Cleaning Pipeline Finished Successfully!")
    return df

if __name__ == "__main__":
    clean_data_pipeline()
