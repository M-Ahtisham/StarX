import streamlit as st
import pandas as pd


# Text Element
st.title("Cars Dataset 🏎️")
st.header("This is a header") # It is smaller than Title
st.subheader("This is a subheader") # It is smaller than Header
st.text("Here is some text that i can write")
st.write("* Hey, this is markdown ")
st.divider()
sliding_val = st.slider("This is a slider",0,100,(50))

df = pd.read_csv("data/Quikr_car.csv",)
st.dataframe(df)
st.write("Drawing a graph of the original data sat without any changes")
st.line_chart(df, x = "Kms_driven", y ="Price")


# Dataset downloaded from
# https://calmcode.io/datasets/bigmac



