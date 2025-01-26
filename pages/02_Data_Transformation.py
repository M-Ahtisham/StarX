import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# This loads the dataset from the session 
df_original = st.session_state.original_df

# This loads the dataset from the session 
df = st.session_state.df_original.copy()           # To be removed
df_transformed = st.session_state.df_original.copy()

# Dropping Unnecessary columns
df_transformed = df_transformed.drop(columns=["Name"])
df_transformed = df_transformed.drop(columns=["No"])

# Transforming the Labels column
label_to_num ={
    "PLATINUM" : 0,
    "GOLD" : 1
}
df_transformed['Label'] = df_transformed['Label'].map(label_to_num)


# Tranforming the Locations column
location_to_num = {
    "Pune": 1,
    "Chennai": 2,
    "Bangalore": 3,
    "Kolkata": 4,
    "Mumbai": 5,
    "Madurai": 6,
    "Hyderabad": 7,
    "Jaipur": 8,
    "Delhi": 9,
    "Trichy": 10,
    "Nagpur": 11,
    "Ahmedabad": 12,
    "NaviMumbai": 13,
    "Lucknow": 14,
    "Kozhikode": 15,
    "Bhubaneswar": 16,
    "Pondicherry": 17,
    "Surat": 18,
    "GirSomnath": 19,
    "Anand": 20,
    "Uttarpara": 21,
    "Muzaffarnagar": 22,
    "Kochi": 23,
    "Dwarka": 24,
    "Udaipur": 25,
    "Bilaspur": 26,
    "Mahasamund": 27,
    "Dhanbad": 28,
    "Malappuram": 29,
    "Nanded": 30,
    "Chandigarh": 31,
    "BolpurSantiniketan": 32,
    "Gurgaon": 33,
    "Kurnool": 34,
    "Thane": 35,
    "Kanchipuram": 36,
    "Coimbatore": 37,
    "Faridabad": 38,
    "Jagdalpur": 39
}

df_transformed['Location'] = df_transformed['Location'].map(location_to_num)
df_transformed['Location'].fillna(40, inplace=True)  # The None values are replaced by 40


# Transforming the Price Column
df_transformed['Price'] = df_transformed['Price'].str.replace('₹', '', regex=False)  # Remove ₹ symbol
df_transformed['Price'] = df_transformed['Price'].str.replace(',', '', regex=False)  # Remove commas
df_transformed['Price'] = df_transformed['Price'].replace('Ask For Price', pd.NA)  # Handle 'Ask For Price'
df_transformed['Price'] = pd.to_numeric(df_transformed['Price'], errors='coerce')  # Convert to numeric
df_transformed['Price'].fillna(df_transformed['Price'].median(), inplace=True)  # Fill NaN with median
df_transformed['Price'] = df_transformed['Price'].astype(int)  # Convert to integers

# Transforming Kms_driven Column
df_transformed['Kms_driven'] = df_transformed['Kms_driven'].str.replace('kms', '', regex=False)  # Remove 'kms'
df_transformed['Kms_driven'] = df_transformed['Kms_driven'].str.replace(',', '', regex=False)  # Remove commas
df_transformed['Kms_driven'] = pd.to_numeric(df_transformed['Kms_driven'], errors='coerce')  # Convert to numeric

# Transforming Fuel_type Column
fuel_type_to_num ={
    "Petrol" : 1,
    "Diesel" : 2,
    "CNG" : 3,
    "Electric" : 4,
    "Petrol + CNG" :5,
    "LPG" : 6,
    "Hybrid" : 7
}
df_transformed['Fuel_type'] = df_transformed['Fuel_type'].map(fuel_type_to_num)

# Transforming Owner Column
owner_to_num = {
    " 1st Owner" : 1,
    " 2nd Owner" : 2,
    " 3rd Owner" : 3,
}
df_transformed['Owner'] = df_transformed['Owner'].map(owner_to_num)
df_transformed['Owner'].fillna(0, inplace=True)  # The None values are replaced by 0

# Transformation of the Company Column
company_to_num = {
    'Maruti': 1,
    'Hyundai': 2,
    'Honda': 3,
    'Ford': 4,
    'Tata': 5,
    'Renault': 6,
    'Mahindra': 7,
    'Toyota': 8,
    'MG': 9,
    'Volkswagen': 10,
    'Jeep': 11,
    'Kia': 12,
    'BMW': 13,
    'Skoda': 14,
    'Nissan': 15,
    'Audi': 16,
    'Datsun': 17,
    'Mercedes': 18,
    'Fiat': 19,
    'Volvo': 20,
    'Jaguar': 21,
    'SsangYong': 22,
    'Land Rover': 23,
    'Porsche': 24
}
df_transformed['Company'] = df_transformed['Company'].map(company_to_num)
df_transformed['Company'].fillna(25, inplace=True)  # The None values are replaced by 0

# Display Transfornmed Data
st.header("Transformed DataFrame")
st.dataframe(df_transformed)

# Display Summary Information
st.subheader("Data Summary and Statistics")
st.write(df_transformed.describe())

st.markdown("## Correlations of features")
st.dataframe(df_transformed.corr().style.background_gradient(cmap='RdYlGn', axis=None)) # The styling was added using seaborn


st.write("## Data types")
st.write(df_transformed.dtypes)

st.markdown("### Graph of Years against Kms_Driven")
st.plotly_chart(px.scatter(df_transformed, x ='Year', y='Kms_driven'))
st.write("The scatter plot indicates a clear trend where older cars tend to have higher kilometers driven, while newer models generally exhibit lower mileage.")
st.write("We can also notice some outliers, most notably is the car with 690,000Kms driven.")

st.markdown("### Graph of Years against Price")
st.plotly_chart(px.scatter(df_transformed, x ='Year', y='Price'))
st.write("The scatter plot indicates a clear trend where newer cars are more expensive then older cars.")
st.write("We can also notice an outlier, most notable one is the car with a price of 7,500,000 INR. These are removed in the next page.")

st.session_state["df_transformed"] = df_transformed

