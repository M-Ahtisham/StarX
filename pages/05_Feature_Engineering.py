import streamlit as st
import pandas as pd
import copy


df_processed = st.session_state.df_processed.copy()

st.markdown("# Selecting feature variables.")
df_processed = df_processed.drop(columns=["Company"])
st.dataframe(df_processed)
st.write("The Company column was dropped")

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)