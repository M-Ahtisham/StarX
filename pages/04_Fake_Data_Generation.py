import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import random
import copy

def main():
    # Header
    st.markdown("# Fake Data Generator")
    
    st.markdown("### Data Randomization")
    st.write("This page generates synthetic data by randomly creating rows based on the ranges and patterns observed in the original dataset.")

    st.write("Click on the button below to create a random dataset")
    
    # Loads the processed data from the session state
    df_processed = st.session_state.df_processed.copy()
    
        
    # Generate random data based on the cleaned dataset
    PRICE_MIN = df_processed['Price'].min()
    PRICE_MAX = df_processed['Price'].max()
    KMS_MIN = df_processed['Kms_driven'].min()
    KMS_MAX = df_processed['Kms_driven'].max()
    YEAR_MIN = df_processed['Year'].min()
    YEAR_MAX = df_processed['Year'].max()
    
    def random_car_data():
        """Generate a random row based on the dataset statistics."""
        return {
            "Label": random.randint(0, 1),  # Random binary label
            "Location": random.randint(1, 40),  # Random numeric location
            "Price": random.randint(PRICE_MIN, PRICE_MAX),
            "Kms_driven": random.randint(KMS_MIN, KMS_MAX),
            "Fuel_type": random.randint(1, 7),  # Random fuel type (numeric)
            "Owner": random.randint(0, 3),  # Random owner count
            "Year": random.randint(YEAR_MIN, YEAR_MAX),
            "Company": random.randint(1, 25),  # Random company as numeric
        }
    
    df_randomized = pd.DataFrame([random_car_data() for _ in range(500)]) # Creates a randomized dataset
    st.session_state["df_randomized"] = df_randomized
        
    if st.button("Randomize Data"):
        df_randomized = pd.DataFrame([random_car_data() for _ in range(500)]) # Creates a randomized dataset
        st.session_state["df_randomized"] = df_randomized # Updates the data in the session state

        
    cols = st.columns(2)
    cols[0].markdown("### Original Processed Data")
    cols[0].dataframe(df_processed)
    cols[0].markdown("### Data metrics")
    cols[0].dataframe(df_processed.describe())

    cols[1].markdown("### Fake Data")
    cols[1].dataframe(st.session_state.df_randomized)
    cols[1].markdown("### Fake Data metrics")
    cols[1].dataframe(df_randomized.describe())
    
    
if "df_processed" in st.session_state:
    main()
    
else:
    st.error("⚠️ Some variables not found in the session state. Please restart the app or launch the pages in the correct order.")
    
    
if "df_randomized" not in st.session_state:
    st.session_state.df_randomized = pd.DataFrame(columns=df_processed.columns, index=range(1000))


# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)