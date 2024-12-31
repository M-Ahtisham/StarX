import streamlit as st
import plotly.express as px

df_cleaned = st.session_state.df_c

#Removes the outliers
df_cleaned = df_cleaned[df_cleaned['Kms_driven'] != 690000]
df_cleaned = df_cleaned[df_cleaned['Price'] != 7500000]


st.plotly_chart(px.scatter(df_cleaned, x ='Year', y='Kms_driven'))
st.plotly_chart(px.scatter(df_cleaned, x ='Year', y='Price'))