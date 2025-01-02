import streamlit as st
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score

# Page Header
st.header("Regression Analysis with Uploaded Data")

# Upload CSV file
DATA_PATH = 'data/Quikr_car.csv'

if DATA_PATH is not None:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(DATA_PATH)

    # Display the dataset
    st.write("### Dataset Preview")
    st.dataframe(df)

    # Ensure the dataset is numeric
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

    # Select columns for regression
    st.write("### Select Features and Target for Regression")
    feature_columns = st.multiselect("Select feature columns (X)", options=df.columns)
    target_column = st.selectbox("Select target column (Y)", options=df.columns)

    if feature_columns and target_column:
        X = df[feature_columns]
        Y = df[target_column]

        # Train-test split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Linear Regression
        regr = linear_model.LinearRegression()
        regr.fit(X_train, Y_train)
        Y_pred = regr.predict(X_test)

        # Display Coefficients and Model Metrics
        st.write("### Linear Regression Results")
        st.write(f"Coefficients: {regr.coef_}")
        score = regr.score(X_test, Y_test)
        st.write(f"R² Score: {score}")
        cross_val = cross_val_score(regr, X, Y, cv=5)
        st.write(f"Cross-Validation Scores: {cross_val}")

        # Lasso Regression
        alpha = st.slider("Select alpha for Lasso Regression", 0.01, 1.0, step=0.01, value=0.1)
        regr_lasso = linear_model.Lasso(alpha=alpha)
        regr_lasso.fit(X_train, Y_train)
        Y_pred_lasso = regr_lasso.predict(X_test)

        # Display Lasso Metrics
        st.write("### Lasso Regression Results")
        st.write(f"Coefficients: {regr_lasso.coef_}")
        score_lasso = regr_lasso.score(X_test, Y_test)
        st.write(f"Lasso R² Score: {score_lasso}")
        cross_val_lasso = cross_val_score(regr_lasso, X, Y, cv=5)
        st.write(f"Lasso Cross-Validation Scores: {cross_val_lasso}")

    else:
        st.warning("Please select both feature columns (X) and a target column (Y).")
else:
    st.info("Awaiting CSV file upload...")