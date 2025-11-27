import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import LabelEncoder, StandardScaler
import io

# Page configuration
st.set_page_config(page_title="Data Cleaning & Quality Checker", layout="wide")
st.title("🔍 Data Cleaning & Quality Checker")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'cleaned_report' not in st.session_state:
    st.session_state.cleaned_report = None

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV/Excel)", type=["csv", "xlsx", "xls"])

def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

def analyze_data_quality(df):
    report = {
        'shape': df.shape,
        'missing_values': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df)) * 100,
        'duplicates': df.duplicated().sum(),
        'outliers': {},
        'categorical_inconsistencies': {},
        'data_types': df.dtypes
    }

    # Detect outliers for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        outliers = detect_outliers(df, col)
        report['outliers'][col] = len(outliers)

    # Detect categorical inconsistencies
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_values = df[col].value_counts()
        # Identify potential inconsistencies (case, whitespace, etc.)
        if df[col].dtype == "object":
            inconsistent_values = df[col].apply(lambda x: x.strip().lower() if isinstance(x, str) else x).value_counts()
            if len(unique_values) != len(inconsistent_values):
                report['categorical_inconsistencies'][col] = unique_values.index.tolist()

    return report

def clean_data(df, operations):
    df_cleaned = df.copy()
    
    for operation in operations:
        col = operation['column']
        action = operation['action']
        
        if action == "drop_column":
            df_cleaned = df_cleaned.drop(columns=[col])
        elif action == "fill_mean" and pd.api.types.is_numeric_dtype(df_cleaned[col]):
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mean())
        elif action == "fill_median" and pd.api.types.is_numeric_dtype(df_cleaned[col]):
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
        elif action == "fill_mode":
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
        elif action == "drop_rows":
            df_cleaned = df_cleaned.dropna(subset=[col])
        elif action.startswith("outlier_"):
            method = action.split("_")[1]
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            if method == "cap":
                df_cleaned[col] = np.where(df_cleaned[col] < lower_bound, lower_bound, df_cleaned[col])
                df_cleaned[col] = np.where(df_cleaned[col] > upper_bound, upper_bound, df_cleaned[col])
            elif method == "remove":
                df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
        elif action == "standardize_text":
            df_cleaned[col] = df_cleaned[col].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
    
    return df_cleaned

# Process uploaded file
if uploaded_file is not None:
    # Read file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.session_state.df = df
        st.session_state.original_df = df.copy()
        st.success(f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# Main application
if st.session_state.df is not None:
    df = st.session_state.df
    original_df = st.session_state.original_df
    
    # Data quality analysis
    if st.button("Run Data Quality Analysis"):
        with st.spinner("Analyzing data quality..."):
            report = analyze_data_quality(df)
            st.session_state.quality_report = report
    
    if 'quality_report' in st.session_state:
        report = st.session_state.quality_report
        
        # Display data quality report
        st.header("📊 Data Quality Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", report['shape'][0])
        col2.metric("Total Columns", report['shape'][1])
        col3.metric("Duplicate Rows", report['duplicates'])
        
        # Missing values
        st.subheader("Missing Values")
        missing_df = pd.DataFrame({
            'Column': report['missing_values'].index,
            'Count': report['missing_values'].values,
            'Percentage': report['missing_percentage'].values
        })
        st.dataframe(missing_df.style.format({'Percentage': '{:.2f}%'}))
        
        # Outliers
        st.subheader("Outliers")
        outlier_df = pd.DataFrame({
            'Column': list(report['outliers'].keys()),
            'Count': list(report['outliers'].values())
        })
        st.dataframe(outlier_df)
        
        # Categorical inconsistencies
        if report['categorical_inconsistencies']:
            st.subheader("Categorical Inconsistencies")
            for col, values in report['categorical_inconsistencies'].items():
                st.write(f"**{col}**: {values}")
        
        # Recommendations
        st.subheader("Recommended Actions")
        recommendations = []
        
        # Missing values recommendations
        for col in missing_df[missing_df['Count'] > 0]['Column']:
            if missing_df[missing_df['Column'] == col]['Percentage'].iloc[0] > 50:
                recommendations.append(f"Drop column '{col}' (more than 50% missing)")
            else:
                recommendations.append(f"Fill missing values in '{col}' (use mean/median/mode)")
        
        # Outlier recommendations
        for col, count in report['outliers'].items():
            if count > 0:
                recommendations.append(f"Handle outliers in '{col}' (cap/remove)")
        
        # Duplicates
        if report['duplicates'] > 0:
            recommendations.append("Remove duplicate rows")
        
        # Categorical inconsistencies
        for col in report['categorical_inconsistencies'].keys():
            recommendations.append(f"Standardize text values in '{col}' (trim/case)")
        
        for rec in recommendations:
            st.write(f"- {rec}")
        
        # Data transformations
        st.header("🔧 Apply Data Transformations")
        operations = []
        
        with st.form("cleaning_form"):
            # Missing value handling
            st.subheader("Handle Missing Values")
            missing_cols = missing_df[missing_df['Count'] > 0]['Column'].tolist()
            for col in missing_cols:
                col_type = df[col].dtype
                if pd.api.types.is_numeric_dtype(df[col]):
                    action = st.selectbox(f"Action for missing values in '{col}'", 
                                          ["fill_mean", "fill_median", "fill_mode", "drop_rows", "no_change"], 
                                          key=f"missing_{col}")
                else:
                    action = st.selectbox(f"Action for missing values in '{col}'", 
                                          ["fill_mode", "drop_rows", "no_change"], 
                                          key=f"missing_{col}")
                
                if action != "no_change":
                    operations.append({"column": col, "action": action})
            
            # Outlier handling
            st.subheader("Handle Outliers")
            outlier_cols = outlier_df[outlier_df['Count'] > 0]['Column'].tolist()
            for col in outlier_cols:
                action = st.selectbox(f"Action for outliers in '{col}'", 
                                      ["outlier_cap", "outlier_remove", "no_change"], 
                                      key=f"outlier_{col}")
                
                if action != "no_change":
                    operations.append({"column": col, "action": action})
            
            # Text standardization
            st.subheader("Text Standardization")
            categorical_cols = [col for col in df.columns if df[col].dtype == "object"]
            for col in categorical_cols:
                if col in report['categorical_inconsistencies']:
                    action = st.selectbox(f"Standardize text in '{col}'", 
                                          ["standardize_text", "no_change"], 
                                          key=f"text_{col}")
                    
                    if action != "no_change":
                        operations.append({"column": col, "action": action})
            
            # Column removal
            st.subheader("Remove Columns")
            cols_to_drop = st.multiselect("Select columns to remove", df.columns.tolist())
            for col in cols_to_drop:
                operations.append({"column": col, "action": "drop_column"})
            
            submitted = st.form_submit_button("Apply Transformations")
        
        if submitted:
            df_cleaned = clean_data(df, operations)
            st.session_state.df = df_cleaned
            st.success("Transformations applied successfully!")
            
            # Generate cleaning report
            report_text = f"""
            # Data Cleaning Report
            
            ## Summary
            - Original shape: {original_df.shape}
            - Cleaned shape: {df_cleaned.shape}
            - Operations applied: {len(operations)}
            
            ## Applied Operations
            """
            for op in operations:
                report_text += f"- {op['action']} on column '{op['column']}'\n"
            
            st.session_state.cleaned_report = report_text
            
            # Show cleaned data preview
            st.subheader("Cleaned Data Preview")
            st.dataframe(df_cleaned.head())
    
    # Download cleaned dataset
    if st.session_state.df is not None:
        st.header("💾 Export Results")
        df_cleaned = st.session_state.df
        csv = df_cleaned.to_csv(index=False)
        st.download_button(
            label="Download Cleaned Dataset (CSV)",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )
        
        # Download report
        if st.session_state.cleaned_report:
            st.download_button(
                label="Download Cleaning Report (TXT)",
                data=st.session_state.cleaned_report,
                file_name="cleaning_report.txt",
                mime="text/plain"
            )

# Show original data if loaded
if st.session_state.original_df is not None:
    st.header("📄 Original Data Preview")
    st.dataframe(st.session_state.original_df.head())
