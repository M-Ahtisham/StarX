import streamlit as st
import pandas as pd
import copy
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load the DataFrame from session state
df_processed = st.session_state.df_processed.copy()

# Feature Engineering Header
st.markdown("# Feature Engineering")

# Step 1: Drop a column interactively
drop_col = st.multiselect("Select columns to drop:", df_processed.columns)
if drop_col:
    df_processed = df_processed.drop(columns=drop_col)
    st.write(f"Columns dropped: {', '.join(drop_col)}")

# Step 2: Add a derived column (example: Total Cost = Salary + Bonus)
if "Salary" in df_processed.columns and "Bonus" in df_processed.columns:
    df_processed["Total Cost"] = df_processed["Salary"] + df_processed["Bonus"]
    st.write("Derived column 'Total Cost' added.")

# Step 3: Standardize or normalize numeric columns
scaling_option = st.radio("Apply scaling:", ["None", "Standardization", "Normalization"])
numeric_cols = df_processed.select_dtypes(include=["float64", "int64"]).columns

if scaling_option == "Standardization":
    scaler = StandardScaler()
    df_processed[numeric_cols] = scaler.fit_transform(df_processed[numeric_cols])
    st.write("Numeric columns standardized.")

elif scaling_option == "Normalization":
    scaler = MinMaxScaler()
    df_processed[numeric_cols] = scaler.fit_transform(df_processed[numeric_cols])
    st.write("Numeric columns normalized.")

# Display the processed DataFrame
st.markdown("## Processed DataFrame")
st.dataframe(df_processed)

# Log feature engineering steps
st.write("Feature engineering steps applied:")
st.write("- Dropped columns:", drop_col)
if "Total Cost" in df_processed.columns:
    st.write("- Added derived column: 'Total Cost'")
st.write("- Applied scaling:", scaling_option)

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Column dropping: Users can interactively select columns to drop.
# Derived column creation: Example of calculating Total Cost from Salary + Bonus.
# Scaling options: Standardization and normalization options for numeric columns.
# Logging: Outputs a summary of all feature engineering steps applied.
