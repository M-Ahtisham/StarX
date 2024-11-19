import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Text Element
st.title("Cars Dataset 🏎️")
st.header("By : ") # It is smaller than Title
st.subheader("Bhatti, Muhammad Ahtisham and Love") # It is smaller than Header
st.text("Different datas for different cars ")
st.write("* We are using Name, Label,Location,price etc as our dataset ")
st.divider()
# sliding_val = st.slider("This is a slider",0,100,(50))

df = pd.read_csv("data/Quikr_car.csv",)
st.dataframe(df)
st.write("Drawing a graph of the original data sat without any changes")
st.line_chart(df, x = "Kms_driven", y ="Price")
st.echarts(df, x = "Kms_driven", y ="Price")



# Dataset downloaded from
# https://calmcode.io/datasets/bigmac



