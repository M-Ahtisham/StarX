# 🚀 Import necessary libraries
import streamlit as st  # 🌐 For creating the web app
import pandas as pd  # 📊 For data manipulation and analysis
from PIL import Image  # 🖼️ To handle image-related tasks
import numpy as np  # 🔢 For numerical computations
from datetime import datetime  # ⏰ To work with date and time
import time  # ⏳ For adding delays if needed
import plotly.express as px  # 📈 For easy data visualizations
import plotly.graph_objects as go  # 🔧 For advanced and custom charts

# 📂 Load the dataset
df = pd.read_csv('data/Quikr_car.csv')  # 🚗 Read the car dataset from a CSV file

# 🖥️ Set the page layout to "wide" for a better, more spacious interface
st.set_page_config(layout="wide")

# 🧱 Divide the page into two columns of equal width
col1, col2 = st.columns([0.5, 0.5])

# 🎨 Add a bar chart in the first column
with col1:
    fig = px.bar(
        df,
        x="Name",  # 🔤 Car names on the x-axis
        y="Company",  # 🏢 Companies on the y-axis
        labels={"Company": "Company {🛞}"},  # 🏷️ Label for the y-axis
        title="Company's in India 🚘",  # 📛 Chart title
        hover_data=["Company"],  # 🖱️ Display company info on hover
        template="gridon",  # 🎨 Simple grid style for aesthetics
        height=500  # 📏 Set chart height
    )
    st.plotly_chart(fig, use_container_width=True)  # 📤 Display the chart

# 📈 Add a scatter plot in the second column
with col2:
    fig1 = px.scatter(
        df,
        x="Kms_driven",  # 🚗 Kilometers driven on the x-axis
        y="Year",  # 📅 Year on the y-axis
        labels={"Year": "Km driven per year 📉"},  # 🏷️ Label for the y-axis
        title="Yearly Driven Data 📊",  # 📛 Chart title
        hover_data=["Kms_driven"],  # 🖱️ Display kilometers on hover
        template="gridon",  # 🎨 Simple grid style
        height=500  # 📏 Set chart height
    )
    st.plotly_chart(fig1, use_container_width=True)  # 📤 Display the chart

# ➖ Add a divider to visually separate sections
st.divider()

# 🧮 Group the dataset by location and count occurrences of fuel type and car names
result1 = (
    df.groupby(by="Location")[["Fuel_type", "Name"]]  # 🗺️ Group by location
    .count()  # 🔢 Count entries in "Fuel_type" and "Name" columns
    .reset_index()  # 📋 Convert "Location" back to a regular column
)

# 🖌️ Create a custom dual-axis chart using Plotly
fig3 = go.Figure()

# 📊 Add a bar chart for the "Fuel_type" column
fig3.add_trace(
    go.Bar(
        x=result1["Location"],  # 🗺️ Locations on the x-axis
        y=result1["Fuel_type"],  # ⛽ Count of fuel types on the y-axis
        name="Fuel_type"  # 🏷️ Legend label
    )
)

# 📈 Add a line chart for the "Name" column
fig3.add_trace(
    go.Scatter(
        x=result1["Location"],  # 🗺️ Locations on the x-axis
        y=result1["Name"],  # 🔤 Count of car names on the y-axis
        name="Name",  # 🏷️ Legend label
        mode="lines",  # ➖ Line chart mode
        yaxis="y2"  # ➕ Secondary y-axis
    )
)

# 🛠️ Customize the chart layout
fig3.update_layout(
    title="DATA BASED ON LOCATION 📍",  # 📛 Chart title
    xaxis=dict(title="Location"),  # 🗺️ Label for the x-axis
    yaxis=dict(title="Fuel_type", showgrid=False),  # ⛽ Label for the primary y-axis
    yaxis2=dict(title="Name", overlaying="y", side="right"),  # 🔤 Secondary y-axis on the right
    template="gridon",  # 🎨 Simple grid style
    legend=dict(x=1, y=1)  # 📜 Place the legend in the top-right corner
)

# 🧱 Divide the page, with the second column being wider
_, col3 = st.columns([0.1, 1])

# 📤 Add the custom chart to the larger column
with col3:
    st.plotly_chart(fig3, use_container_width=True)  # 📤 Display the dual-axis chart
