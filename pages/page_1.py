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


st.divider()

# Grouping and aggregating data
result1 = (
    df.groupby(by="Location")[["Fuel_type", "Name"]]
    .count()  # Use count or other appropriate aggregation to get DataFrame output
    .reset_index()
)

# Plotly Figure
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["Location"], y=result1["Fuel_type"], name="Fuel_type"))
fig3.add_trace(
    go.Scatter(
        x=result1["Location"],
        y=result1["Name"],
        name="Name",
        mode="lines",
        yaxis="y2",
    )
)

fig3.update_layout(
    title="DATA BASED ON LOCATION",
    xaxis=dict(title="Location"),
    yaxis=dict(title="Fuel_type", showgrid=False),
    yaxis2=dict(title="Name", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1),
)

# Display Plotly chart
_, col3 = st.columns([0.1, 1])
with col3:
    st.plotly_chart(fig3, use_container_width=True)
  