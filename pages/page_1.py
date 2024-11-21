import streamlit as st
import pandas as pd
# from streamlit_echarts import st_echarts
from PIL import Image
import numpy as np 
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go 





df = pd.read_csv('data/Quikr_car.csv')
st.set_page_config(layout="wide")


col1,col2=st.columns([0.5,0.5])

  
with col1:
    fig = px.bar(df, x="Name", y= "Company", labels = {"Company": "Company{🛞}"},
                title= "Company's in India", hover_data=["Company"],
                template="gridon", height =500 )
    st.plotly_chart(fig,use_container_width=True)

with col2:
      fig1 = px.scatter(df, x="Kms_driven", y= "Year", labels = {"Year": "Km driven per year"},
                title= "Yearly Driven data", hover_data=["Kms_driven"],
                template="gridon", height =500 )
      st.plotly_chart(fig1,use_container_width=True)
