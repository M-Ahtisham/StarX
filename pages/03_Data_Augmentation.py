# import pandas as pd
# import numpy as np
# import streamlit as st

# st.header("Fake Data")

# df_cleaned = st.session_state.df_c

# def generate_fake_row():
#     # Generate random data for a single row
#     row = {
#         "Label": np.random.randint(0, 2),
#         "Location": np.random.randint(0, 10),
#         "Price": np.random.randint(100000, 4000000),
#         "Kms_driven": np.random.randint(1000, 200000),
#         "Fuel_type": np.random.randint(0, 4),
#         "Owner": np.random.randint(0, 3),
#         "Year": np.random.randint(2000, 2023),
#         "Company": np.random.randint(0, 20)
#     }
#     return row

# # Set the number of rows you want for the fake dataset
# num_rows = int(len(df_cleaned) * 0.4)

# # Generate the fake dataset iteratively
# fake_data = []
# for _ in range(num_rows):
#     fake_data.append(generate_fake_row())




# # Create the DataFrame with the generated data
# df_fake = pd.DataFrame(fake_data)

# st.write(df_fake)

import pandas as pd
import numpy as np
import streamlit as st
import random

# Streamlit Header
st.header("Fake Data Generator")

# Load the dataset
DATA_PATH = 'data/Quikr_car.csv'

try:
    # Load the dataset while skipping problematic rows
    df = pd.read_csv(DATA_PATH, on_bad_lines='skip')

    # Clean the 'Price' column (remove currency symbols, commas, and convert to numeric)
    df['Price'] = pd.to_numeric(df['Price'].str.replace('[₹,]', '', regex=True), errors='coerce')
    df = df.dropna(subset=['Price'])  # Drop rows where Price is NaN

    # Clean the 'Kms_driven' column (remove commas, units, and convert to numeric)
    df['Kms_driven'] = pd.to_numeric(df['Kms_driven'].str.replace(',', '').str.replace(' kms', '', regex=True), errors='coerce')

    # Drop rows with NaN in critical numeric columns
    df = df.dropna(subset=['Kms_driven'])

    # Ensure the 'Year' column is numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])

except FileNotFoundError:
    st.error(f"File not found: {DATA_PATH}")
    st.stop()
except KeyError as e:
    st.error(f"Missing expected column in dataset: {e}")
    st.stop()

# Generate random data based on the cleaned dataset
PRICE_MIN = df['Price'].min()
PRICE_MAX = df['Price'].max()
KMS_MIN = df['Kms_driven'].min()
KMS_MAX = df['Kms_driven'].max()
YEAR_MIN = df['Year'].min()
YEAR_MAX = df['Year'].max()

def random_car_data():
    """Generate a random row based on the dataset statistics."""
    return {
        "Label": random.randint(0, 1),  # Random binary label
        "Location": random.randint(1, 10),  # Random numeric location
        "Price": round(random.uniform(PRICE_MIN, PRICE_MAX), 2),
        "Kms_driven": random.randint(KMS_MIN, KMS_MAX),
        "Fuel_type": random.randint(0, 3),  # Random fuel type (numeric)
        "Owner": random.randint(1, 5),  # Random owner count
        "Year": random.randint(YEAR_MIN, YEAR_MAX),
        "Company": random.randint(1, 20),  # Random company as numeric
    }

def generate_fake_data(rows=1000):
    """Generate a DataFrame of random data."""
    return pd.DataFrame([random_car_data() for _ in range(rows)])

# Streamlit App
def main():
    st.sidebar.header("Settings")
    num_rows = st.sidebar.slider("Number of Fake Data Rows", min_value=10, max_value=5000, value=1000, step=10)

    # Display original data
    st.markdown("## Original Data")
    # st.dataframe(df.head())
    df = pd.read_csv(DATA_PATH )
    df = df.drop('No',axis=1)
    st.dataframe(df)

    # Display cleaned data
    # st.markdown("## Cleaned Data")
    # st.dataframe(df)

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

    

    # Generate and display fake data
    if st.button("Generate Fake Data"):
        with st.spinner("Generating fake data..."):
            fake_data = generate_fake_data(rows=num_rows)
        st.success("Fake data generated successfully!")

        # Display a randomized table
        st.markdown("## Randomized Data Table")
        randomized_data = fake_data.sample(frac=1).reset_index(drop=True)  # Shuffle rows
        st.dataframe(randomized_data)


        # Display fake data
        st.markdown("## Fake Data")
        st.dataframe(fake_data)

        # Display metrics for fake data
        st.markdown("### Fake Data Metrics")
        st.dataframe(fake_data.describe())

      

        # Allow downloading fake data as CSV
        csv = fake_data.to_csv(index=False).encode("utf-8")
        st.download_button("Download Fake Data as CSV", data=csv, file_name="fake_car_data.csv", mime="text/csv")

if __name__ == "__main__":
    main()