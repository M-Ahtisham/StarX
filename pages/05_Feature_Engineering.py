import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Load the initial DataFrame from session state
if "df_engineered" not in st.session_state:
    st.session_state.df_engineered = st.session_state.df_processed.copy()

df_engineered = st.session_state.df_engineered

# Feature Engineering Header
st.markdown("# Feature Engineering")

# Step 1: Add derived columns
def add_derived_columns():
    df = st.session_state.df_engineered
    if {"Year", "Kms_driven", "Owner"}.issubset(df.columns):
        current_year = 2025
        max_age = 25
        max_kms = 200000
        max_owners = 3

        df["Age"] = current_year - df["Year"]
        df["Condition Score"] = (
            (0.4 * (1 - df["Age"] / max_age)) +
            (0.4 * (1 - df["Kms_driven"] / max_kms)) +
            (0.2 * (1 - df["Owner"] / max_owners))
        )
        st.session_state.df_engineered = df

# Callback function to handle column removal
def remove_columns():
    drop_col = st.session_state.get("drop_col", [])
    if drop_col:
        st.session_state.df_engineered = st.session_state.df_engineered.drop(columns=drop_col)
        st.write(f"Columns dropped: {', '.join(drop_col)}")
        

# Reset button logic
if st.button("Reset"):
    st.session_state.df_engineered = st.session_state.df_processed.copy()
    add_derived_columns()

# Add derived columns on load or reset
add_derived_columns()

# Step 2: Interactive column dropping
st.multiselect(
    "Select columns to drop:",
    options=st.session_state.df_engineered.columns,
    key="drop_col",
    on_change=remove_columns,  # Pass the callback function
)

# Step 3: Scaling options
scaling_option = st.radio("Apply scaling:", ["None", "Standardization", "Normalization"])
numeric_cols = st.session_state.df_engineered.select_dtypes(include=["float64", "int64"]).columns

if scaling_option == "Standardization":
    scaler = StandardScaler()
    st.session_state.df_engineered[numeric_cols] = scaler.fit_transform(st.session_state.df_engineered[numeric_cols])
    st.write("Numeric columns standardized.")

elif scaling_option == "Normalization":
    scaler = MinMaxScaler()
    st.session_state.df_engineered[numeric_cols] = scaler.fit_transform(st.session_state.df_engineered[numeric_cols])
    st.write("Numeric columns normalized.")
    

# Display the processed DataFrame
st.markdown("## Processed DataFrame")
st.dataframe(st.session_state.df_engineered)

# Log feature engineering steps
st.write("Feature engineering steps applied:")
if "Age" in st.session_state.df_engineered.columns and "Condition Score" in st.session_state.df_engineered.columns:
    st.write("- Added derived columns: 'Age' and 'Condition Score'")
if scaling_option != "None":
    st.write(f"- Applied scaling: {scaling_option}")
if st.session_state.get("drop_col"):
    st.write(f"- Dropped columns: {', '.join(st.session_state['drop_col'])}")
    

st.session_state.df_engineered = df_engineered