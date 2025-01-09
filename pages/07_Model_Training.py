import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split

# Page Header
st.header("Model Training and Predictions")

# Upload CSV file
uploaded_file = 'data/Quikr_car.csv'

if uploaded_file is not None:
    # Load and clean the dataset
    df = pd.read_csv(uploaded_file)

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

    # Feature and Target Selection
    st.write("### Select Features and Target for Training")
    feature_columns = st.multiselect("Select feature columns (X)", options=df.columns)
    target_column = st.selectbox("Select target column (Y)", options=df.columns)

    if feature_columns and target_column:
        X = df[feature_columns]
        Y = df[target_column]

        # Train-test split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Train Linear Regression Model
        regr = linear_model.LinearRegression()
        regr.fit(X_train, Y_train)

        # Predictions and Evaluation
        Y_pred = regr.predict(X_test)
        score = regr.score(X_test, Y_test)

        st.write("### Model Results")
        st.success(f"Model trained successfully! R² Score: {score:.2f}")
        st.write("#### Coefficients:")
        st.write(regr.coef_)

        # User Input for Predictions
        st.write("### Make Predictions")
        input_values = {}
        for col in feature_columns:
            input_values[col] = st.number_input(f"Enter value for {col}", value=float(X[col].mean()))

        if st.button("Predict"):
            input_data = pd.DataFrame([input_values])
            prediction = regr.predict(input_data)
            st.write(f"#### Predicted Value: {prediction[0]:.2f}")

        # Visualizations
        st.write("### Visualization")
        fig, ax = plt.subplots()
        ax.scatter(X_test[feature_columns[0]], Y_test, color="blue", label="Actual")
        ax.scatter(X_test[feature_columns[0]], Y_pred, color="red", label="Predicted")
        ax.set_xlabel(feature_columns[0])
        ax.set_ylabel(target_column)
        ax.legend()
        st.pyplot(fig)

    else:
        st.warning("Please select both features and target columns.")
else:
    st.info("Awaiting CSV file upload...")


# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)
