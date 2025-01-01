import pandas as pd
import streamlit as st

#This is a Custom Styling
st.markdown(
    """
    <style>
    :root {
        --sidebar-text-color: #000000;      /* Default text color for light mode */
        --sidebar-bg-color: #e8edf1;       /* Default background color for light mode */
        --sidebar-highlight-color: #d6e4f5; /* Light blue tint for light mode */
    }

    [data-testid="stSidebarContent"] {
        color: var(--sidebar-text-color);  /* Dynamic Sidebar text color */
        background-color: var(--sidebar-bg-color);  /* Dynamic Sidebar background */
        font-family: 'Arial', sans-serif;  /* Stylish font */
        padding: 15px;  /* Adds some padding */
        border-radius: 10px;  /* Smooth corner style */
        border: 2px solid var(--sidebar-highlight-color); /* Blue highlight border */
        box-shadow: 0px 4px 8px var(--sidebar-highlight-color); /* Blue shadow effect */
    }

    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        :root {
            --sidebar-text-color: #ffffff;  /* Text color for dark mode */
            --sidebar-bg-color: #333333;   /* Background color for dark mode */
            --sidebar-highlight-color: #4a90e2; /* Dark blue tint for dark mode */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load the CSV file into a DataFrame
file_path = 'data/Quikr_car.csv'  # Replace with your correct path
df = pd.read_csv(file_path)

# Display Original DataFrame
st.title("Quikr Car Data")
st.header("Original DataFrame")
df = df.drop('No',axis=1)
st.dataframe(df)

# Step 1: Clean the 'Price' Column
df['Price'] = df['Price'].replace('[₹,]', '', regex=True)
df['Price'] = df['Price'].replace('Ask For Price', pd.NA)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
# Fill NaN values with the median price
df['Price'].fillna(df['Price'].median(), inplace=True)

# Step 2: Clean the 'Kms_driven' Column
df['Kms_driven'] = df['Kms_driven'].replace(' kms', '', regex=True).replace(',', '', regex=True)
df['Kms_driven'] = pd.to_numeric(df['Kms_driven'], errors='coerce')

# Step 3: Encode Categorical Columns
categorical_columns = ['Label', 'Location', 'Fuel_type', 'Owner', 'Company']

# Fill missing values with "Unknown"
df[categorical_columns] = df[categorical_columns].fillna('Unknown')

# Encode categorical columns using Pandas factorize
for col in categorical_columns:
    df[col] = pd.factorize(df[col])[0]

# Step 4: Drop Unnecessary Columns
df_cleaned = df.drop(columns=['Name', 'Unnamed: 0'], errors='ignore')

# Display Cleaned DataFrame
st.header("Cleaned DataFrame")
st.dataframe(df_cleaned)

# Display Summary Information
st.subheader("Data Summary and Statistics")
st.write(df_cleaned.describe())

st.markdown("## Correlations of features")
st.write(df_cleaned.corr())

if 'df_c' not in st.session_state:
    st.session_state['df_c'] = df_cleaned

