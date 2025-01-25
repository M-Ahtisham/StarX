import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Copy the original processed and randomized DataFrames
df_processed = st.session_state.df_processed.copy()
df_random = st.session_state.df_randomized.copy()

# Title
st.title("Predictions on Augmented Data")

# Add a slider to select the percentage of fake data
fake_data_percentage = st.slider(
    "Select the percentage of fake/random data to include:",
    min_value=25,
    max_value=50,
    value=25,  # Default value
    step=1,
    format="%d%%"
)

# Calculate the number of fake rows based on the percentage
num_fake_rows = int(len(df_processed) * (fake_data_percentage / 100))

# Select the required number of rows from the random DataFrame
df_fake = df_random.sample(n=num_fake_rows, random_state=42)

# Create the augmented DataFrame
df_augmented = pd.concat([df_processed, df_fake]).reset_index(drop=True)

# Display the augmented DataFrame
st.write("## Augmented DataFrame:")
st.dataframe(df_augmented)
st.write(" This is a dataframe that contains both the original data, and fake data added to it's end.")


