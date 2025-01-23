import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import random
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Helper function to generate random car data
def random_car_data(year_range):
    return {
        "Year": random.randint(year_range[0], year_range[1]),
        "Location": random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]),
        "Company": random.choice(list(company_mapping.keys())),
        "Fuel_type": random.choice(list(fuel_type_mapping.keys())),
        "Kms_driven": random.randint(10000, 200000),
        "Owner": random.choice(list(owner_mapping.keys())),
        "Price": random.randint(100000, 2000000)
    }

# Mapping for Fuel Types
fuel_type_mapping = {
    1: "Petrol",
    2: "Diesel",
    3: "CNG",
    4: "Electric",
    5: "Petrol + CNG",
    6: "LPG",
    7: "Hybrid"
}

reverse_fuel_type_mapping = {v: k for k, v in fuel_type_mapping.items()}

# Mapping for Owner Types
owner_mapping = {
    "1st Owner": 1,
    "2nd Owner": 2,
    "3rd Owner": 3
}

reverse_owner_mapping = {v: k for k, v in owner_mapping.items()}

# Mapping for Companies
company_mapping = {
    "Maruti": 1,
    "Hyundai": 2,
    "Honda": 3,
    "Ford": 4,
    "Tata": 5,
    "Renault": 6,
    "Mahindra": 7,
    "Toyota": 8,
    "MG": 9,
    "Volkswagen": 10,
    "Jeep": 11,
    "Kia": 12,
    "BMW": 13,
    "Skoda": 14,
    "Nissan": 15,
    "Audi": 16,
    "Datsun": 17,
    "Mercedes": 18,
    "Fiat": 19,
    "Volvo": 20,
    "Jaguar": 21,
    "SsangYong": 22,
    "Land Rover": 23,
    "Porsche": 24
}

reverse_company_mapping = {v: k for k, v in company_mapping.items()}

# Load the original DataFrame from session state
df_processed = st.session_state.df_processed.copy()

# Get the year range from the original data
year_range = (int(df_processed["Year"].min()), int(df_processed["Year"].max()))

# Generate 25-50% fake data
fake_data_percentage = random.uniform(0.25, 0.5)
num_fake_rows = int(len(df_processed) * fake_data_percentage)
fake_data = pd.DataFrame([random_car_data(year_range) for _ in range(num_fake_rows)])
for col in ['Year', 'Kms_driven', 'Price']:
    fake_data[col] = fake_data[col].apply(lambda x: x * random.uniform(0.8, 1.2))

# Combine original and fake data
combined_data = pd.concat([df_processed, fake_data], ignore_index=True)

# Ensure proper data types and map descriptive names
combined_data['Fuel_type_label'] = combined_data['Fuel_type'].map(fuel_type_mapping)
combined_data['Owner_label'] = combined_data['Owner'].map(reverse_owner_mapping)
combined_data['Company_label'] = combined_data['Company'].map(reverse_company_mapping)

# Function to analyze the effects of adding fake data
def analyze_effects(original, augmented):
    changes = {}
    for col in ['Year', 'Kms_driven', 'Price']:
        changes[col] = {
            'Original Mean': original[col].mean(),
            'Augmented Mean': augmented[col].mean(),
            'Change (%)': ((augmented[col].mean() - original[col].mean()) / original[col].mean()) * 100
        }
    return pd.DataFrame(changes).T

# Display the differences
st.header("Original vs. Augmented Dataset")
st.write(f"### Percentage of Fake Data Added: {fake_data_percentage * 100:.2f}%")
changes_summary = analyze_effects(df_processed, combined_data)
changes_summary.reset_index(inplace=True)
changes_summary.rename(columns={'index': 'Metric'}, inplace=True)
st.write("### Changes After Adding Fake Data")
st.dataframe(changes_summary)

# Plot changes in the data
st.write("### Visualization of Changes")
fig, ax = plt.subplots(figsize=(8, 5))
changes_summary.set_index('Metric')[['Change (%)']].plot(kind='bar', ax=ax)
ax.set_ylabel('Change (%)')
ax.set_title('Impact of Adding Fake Data')
st.pyplot(fig)

# Sidebar for inputs
st.sidebar.header("Input Features")
year = st.sidebar.slider("Year", year_range[0], year_range[1], 2017)
location = st.sidebar.selectbox("Location", sorted(map(str, combined_data["Location"].unique())))
company_label = st.sidebar.selectbox("Company", sorted(company_mapping.keys()))
fuel_type_label = st.sidebar.radio("Fuel Type", sorted(map(str, fuel_type_mapping.values())), index=0)
kms_driven = st.sidebar.slider("Kms Driven", int(combined_data["Kms_driven"].min()), int(combined_data["Kms_driven"].max()), 40000)
owner_label = st.sidebar.radio("Owner Type", sorted(owner_mapping.keys()), index=0)

# Convert selected fuel type, owner type, and company back to numeric values
fuel_type = reverse_fuel_type_mapping[fuel_type_label]
owner = owner_mapping[owner_label]
company = company_mapping[company_label]

# Prepare data for prediction
X = pd.get_dummies(combined_data[["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"]], drop_first=True)
y = combined_data["Price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Reindex the input data to match columns in X
input_data = pd.DataFrame([[location, kms_driven, fuel_type, owner, year, company]], 
                          columns=["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"])
input_data = pd.get_dummies(input_data, drop_first=True).reindex(columns=X.columns, fill_value=0)

# Lasso Regression
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_pred_input = lasso_model.predict(input_data)[0]

# Ridge Regression
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_pred_input = ridge_model.predict(input_data)[0]

# Display predictions with color highlights
st.header("Predicted Price")

# Define styles for highlighting
lasso_style = "color: #FFFFFF; background-color: #FF5733; padding: 10px; border-radius: 5px;"
ridge_style = "color: #FFFFFF; background-color: #1E90FF; padding: 10px; border-radius: 5px;"

# Display Lasso prediction
st.markdown(
    f"<h3>Lasso Predicted Price: <span style='{lasso_style}'>₹{lasso_pred_input:,.2f}</span></h3>",
    unsafe_allow_html=True
)

# Display Ridge prediction
st.markdown(
    f"<h3>Ridge Predicted Price: <span style='{ridge_style}'>₹{ridge_pred_input:,.2f}</span></h3>",
    unsafe_allow_html=True
)
