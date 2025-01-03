import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Function to generate fake data with column names from the original dataset
def generate_fake_data(column_names, rows=1000):
    """
    Generates a DataFrame with numeric-only fake data matching the original dataset column names.
    Args:
        column_names (list): List of column names from the original dataset.
        rows (int): Number of rows to generate.
    Returns:
        pd.DataFrame: Generated fake dataset.
    """
    data = {col: np.random.randint(1, 1000, size=rows) for col in column_names}
    return pd.DataFrame(data)


# Streamlit app starts here
# Page Header
st.title("Regression Analysis with Real and Fake Data")

# Step 1: Upload Original CSV File
uploaded_file = 'data/Quikr_car.csv'
df = pd.read_csv(uploaded_file)

if uploaded_file:
    # Load original data
    original_data = pd.read_csv(uploaded_file)
    st.subheader("Original Dataset")
    st.dataframe(original_data)

    # Clean the data (unchanged lines 27 to 63)
    df['Price'] = df['Price'].replace('[₹,]', '', regex=True)
    df['Price'] = df['Price'].replace('Ask For Price', pd.NA)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Price'].fillna(df['Price'].median(), inplace=True)

    df['Kms_driven'] = df['Kms_driven'].replace(' kms', '', regex=True).replace(',', '', regex=True)
    df['Kms_driven'] = pd.to_numeric(df['Kms_driven'], errors='coerce')

    categorical_columns = ['Label', 'Location', 'Fuel_type', 'Owner', 'Company']
    df[categorical_columns] = df[categorical_columns].fillna('Unknown')

    for col in categorical_columns:
        df[col] = pd.factorize(df[col])[0]

    df_cleaned = df.drop(columns=['Name', 'Unnamed: 0'], errors='ignore')

    st.header("Cleaned DataFrame")
    st.dataframe(df_cleaned)

    # Extract column names from the original dataset
    column_names = original_data.columns.tolist()

    # Fake Data Generation
    st.subheader("Generate Fake Numeric Data")
    num_rows = st.slider("Number of rows to generate", min_value=100, max_value=5000, step=100, value=1000)

    if "fake_data" not in st.session_state:
        st.session_state.fake_data = pd.DataFrame()

    if st.button("Generate Fake Data"):
        # Generate fake data with the same column names as the original dataset
        st.session_state.fake_data = generate_fake_data(column_names=column_names, rows=num_rows)
        st.success("Fake data generated successfully!")

    # Display fake data and scatter plot
    if not st.session_state.fake_data.empty:
        st.subheader("Generated Fake Data")
        st.dataframe(st.session_state.fake_data)

        # Scatter plot visualization for fake data
        st.subheader("Scatter Plot for Fake Data")
        x_axis = st.selectbox("Select X-axis for Fake Data", options=st.session_state.fake_data.columns)
        y_axis = st.selectbox("Select Y-axis for Fake Data", options=st.session_state.fake_data.columns)

        if x_axis and y_axis:
            fig, ax = plt.subplots()
            ax.scatter(st.session_state.fake_data[x_axis], st.session_state.fake_data[y_axis], alpha=0.5, color="blue")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Scatter Plot: {x_axis} vs {y_axis}")
            st.pyplot(fig)

        # Allow downloading fake data as CSV
        csv = st.session_state.fake_data.to_csv(index=False).encode("utf-8")
        st.download_button("Download Fake Data as CSV", data=csv, file_name="fake_data.csv", mime="text/csv")

        # Proceed to training if fake data is available
        st.header("Train a Model with Data")

        # Feature and Target Selection
        feature_columns = st.multiselect("Select feature columns (X)", options=column_names[:-1])
        target_column = st.selectbox("Select target column (Y)", options=column_names)

        if feature_columns and target_column:
            try:
                # Use cleaned data for feature and target selection
                X = df_cleaned[feature_columns]
                Y = df_cleaned[target_column]

                # Train-test split using cleaned data
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

                # Train a Linear Regression model
                regr = LinearRegression()
                regr.fit(X_train, Y_train)

                # Make predictions using the test set
                Y_pred = regr.predict(X_test)
                score = regr.score(X_test, Y_test)  # Calculate the R² score

                # Display model results
                st.subheader("Model Results")
                st.success(f"Model trained successfully! R² Score: {score:.2f}")
                st.write("Model Coefficients:", regr.coef_)

                # Visualization: Actual vs Predicted
                st.subheader("Visualization: Actual vs Predicted")
                fig, ax = plt.subplots()
                ax.scatter(Y_test, Y_pred, color="blue", alpha=0.5, label="Predicted")  # Scatter plot of predictions
                ax.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], color="red", linewidth=2, label="Perfect Fit")  # Reference line
                ax.set_xlabel("Actual Values")
                ax.set_ylabel("Predicted Values")
                ax.legend()
                st.pyplot(fig)

                # Section 3: User Input for Predictions
                st.subheader("Make Predictions")
                input_values = {}  # Dictionary to store user inputs
                for col in feature_columns:
                    input_values[col] = st.number_input(f"Enter value for {col}", float(X[col].min()), float(X[col].max()), float(X[col].mean()))

                # Button to make predictions based on user input
                if st.button("Predict"):
                    input_df = pd.DataFrame([input_values])  # Convert user input to DataFrame
                    prediction = regr.predict(input_df)  # Make prediction
                    st.success(f"Predicted Value: {prediction[0]:.2f}")  # Display the predicted value

            except Exception as e:
                # Handle any errors during model training or prediction
                st.error(f"An error occurred: {e}")
        else:
            # Warn the user if they haven't selected features and target
            st.warning("Please select both feature columns (X) and a target column (Y).")

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
