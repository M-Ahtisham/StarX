import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib
import seaborn as sns
import copy


st.header("Removing outliers")
df_transformed = st.session_state.df_transformed
df_processed = df_transformed.copy() # Creates a copy of the transformed dataset

# Remove rows that are more than 99 percentile for Kms_driven
df_processed = df_processed[df_processed['Kms_driven'] <= df_processed['Kms_driven'].quantile(0.99)]

# Remove rows that are more than 99 percentile for Price
df_processed = df_processed[df_processed['Price'] <= df_processed['Price'].quantile(0.98)]

st.write("### Processed DataFrame after outliers removal")
st.dataframe(df_processed)

st.markdown("### Graph of Years against Kms_Driven for Processed Data")
st.plotly_chart(px.scatter(df_processed, x ='Year', y='Kms_driven'))

st.markdown("### Graph of Years against Price for Processed Data")
st.plotly_chart(px.scatter(df_processed, x ='Year', y='Price'))

cols = st.columns(2)
cols[0].markdown("## Transformed data")
cols[0].dataframe(df_transformed)
cols[0].write("###### Unprocessed data that has outliers")
cols[0].markdown("### Data metrics")
cols[0].dataframe(df_transformed.describe())

cols[1].markdown("## Processed data")
cols[1].dataframe(df_processed)
cols[1].write("###### Processed data with outliers removed")
cols[1].markdown("### Processed Data metrics")
cols[1].dataframe(df_processed.describe())

st.session_state["df_processed"] = df_processed

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)