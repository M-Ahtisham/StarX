import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from PIL import Image
import numpy as np 
import time



#spinner 
with st.spinner("waiting.."):
    time.sleep(2)
st.success("Welcome to ")

# Text Element
st.title("Project StarX 🏎️")
st.header("By : ") # It is smaller than Title
st.subheader(" Muhammad Ahtisham and Love") # It is smaller than Header
st.info("* We are using Name, Label,Location,price etc as our dataset ")
img =Image.open("demopic.jpg")
st.image(img)
st.divider()
sliding_val = st.slider("This is a slider",0,100,(50))

df = pd.read_csv("data/Quikr_car.csv",)
st.dataframe(df)
st.write("Drawing a graph of the original data sat without any changes")
st.line_chart(df, x = "Kms_driven", y ="Price")
st.echarts(df, x = "Kms_driven", y ="Price")



# Dataset downloaded from
# https://calmcode.io/datasets/bigmac



