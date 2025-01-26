import streamlit as st
import plotly.express as px

# This loads the dataset from the session 
df_original = st.session_state.original_df

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)
st.title("Quikr Car Data")

# Display Original DataFrame
st.header("Original DataFrame")
st.dataframe(df_original.drop('No',axis=1))

st.write("The Dataset has 9 columns, 3 of which are numeric and 6 are in words.")

st.header("DataFrame Overview")

st.markdown("### Label column overview")
label_counts = df_original['Label'].value_counts().reset_index()
label_counts.columns = ['Label', 'Count']  # Rename columns for clarity
fig_1 = px.bar(label_counts, x='Label', y='Count', title='Count of Labels', text='Count')
st.plotly_chart(fig_1)
st.write("The distribution of labels, where the PLATINUM category has a significantly higher count (688) compared to the GOLD category (344). It highlights a nearly 2:1 ratio in favor of the PLATINUM label.")

st.markdown("### Location column overview")
label_counts = df_original['Location'].value_counts().reset_index()
label_counts.columns = ['Location', 'Count']  # Rename columns for clarity
fig_2 = px.bar(label_counts, x='Location', y='Count', title='Count of Cars by Locations', text='Count')
st.plotly_chart(fig_2)
st.write("The majority of used cars are concentrated in three cities: Pune, Chennai, and Bangalore, while the remaining cities contribute significantly fewer cars.")

st.markdown("### Fuel Type column overview")
df_original['Fuel_type'] = df_original['Fuel_type'].str.strip() # Removes leading/trailing spaces
label_counts = df_original['Fuel_type'].value_counts().reset_index()
label_counts.columns = ['Fuel_type', 'Count']  # Rename columns for clarity
fig_3 = px.bar(label_counts, x='Fuel_type', y='Count', title='Count of Cars by Fuel Type', text='Count')
st.plotly_chart(fig_3)
st.write("The graph highlights that petrol-powered vehicles dominate the dataset, followed by diesel vehicles. Other fuel types, such as CNG, electric, and hybrids, make up a negligible portion, indicating their limited presence in the used car market.")

st.markdown("### Owner column overview")
label_counts = df_original['Owner'].value_counts().reindex([' 1st Owner', ' 2nd Owner', ' 3rd Owner']).reset_index()
label_counts.columns = ['Owner', 'Count']  # Rename columns for clarity
fig_4 = px.bar(label_counts, x='Owner', y='Count', title='Count of Cars by Owner', text='Count')
st.plotly_chart(fig_4)
st.write("The majority of cars are 2nd Owner, followed by fewer 1st Owner cars, while 3rd Owner cars are very rare.")

st.markdown("### Year column overview")
label_counts = df_original['Year'].value_counts().reset_index()
label_counts.columns = ['Year', 'Count']  # Rename columns for clarity
fig_5 = px.bar(label_counts, x='Year', y='Count', title='Count of Cars by Year', text='Count')
st.plotly_chart(fig_5)
st.write("The majority of cars were manufactured between 2016 and 2018, while the number of cars from other years is significantly lower.")

st.markdown("### Company column overview")
label_counts = df_original['Company'].value_counts().reset_index()
label_counts.columns = ['Company', 'Count']  # Rename columns for clarity
fig_6 = px.bar(label_counts, x='Company', y='Count', title='Count of Cars by Company', text='Count')
st.plotly_chart(fig_6)
st.write("Maruti has the highest number of cars (384), followed by Hyundai (228), and others. The data reflects the distribution of cars across various companies, with a sharp decline in counts after the top few brands.")


# Store the original dataframe in the session state
st.session_state["df_original"] = df_original


