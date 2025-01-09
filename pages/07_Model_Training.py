import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Load the DataFrame from session state
if "df_processed" in st.session_state:
    df_processed = st.session_state.df_processed.copy()
else:
    st.error("No data found in session state. Please upload and process data first.")
    st.stop()

# Page Header
st.header("📈 Model Training and Predictions")

# Feature and Target Selection
st.write("### 🔧 Select Features and Target for Training")
feature_columns = st.multiselect("📌 Select feature columns (X)", options=df_processed.columns)
target_column = st.selectbox("🎯 Select target column (Y)", options=df_processed.columns)

# Train-Test Split Slider
st.write("### ⚙️ Train-Test Split Ratio")
train_size = st.slider("Select training set size (%)", 50, 90, 80) / 100

if feature_columns and target_column:
    # Prepare data
    X = df_processed[feature_columns]
    Y = df_processed[target_column]

    # Train-test split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1-train_size, random_state=42)

    # Model Selection
    st.write("### 🤖 Select Regression Model")
    model_type = st.selectbox("Choose model type", ["Linear Regression", "Ridge Regression", "Lasso Regression"])

    # Hyperparameter Slider for Ridge/Lasso
    alpha = 1.0
    if model_type != "Linear Regression":
        alpha = st.slider("Select Regularization Strength (Alpha)", 0.01, 10.0, 1.0)

    # Model Training
    if model_type == "Linear Regression":
        model = linear_model.LinearRegression()
    elif model_type == "Ridge Regression":
        model = linear_model.Ridge(alpha=alpha)
    else:
        model = linear_model.Lasso(alpha=alpha)

    model.fit(X_train, Y_train)

    # Predictions and Evaluation
    Y_pred = model.predict(X_test)
    r2_score = model.score(X_test, Y_test)

    # Calculate error metrics
    mae = mean_absolute_error(Y_test, Y_pred)
    mse = mean_squared_error(Y_test, Y_pred)
    rmse = np.sqrt(mse)

    # Visualizations
    st.write("### 📊 Visualizations")

    # Create columns for side-by-side charts
    col1, col2 = st.columns(2)

    # Scatter Plot for Actual vs. Predicted
    with col1:
        st.write("#### 📈 Actual vs. Predicted")
        fig1, ax1 = plt.subplots()
        ax1.scatter(Y_test, Y_pred, color="#6a0dad")
        ax1.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], "--", color="#ff4500")
        ax1.set_xlabel("Actual Values")
        ax1.set_ylabel("Predicted Values")
        ax1.set_title("Actual vs. Predicted Values")
        st.pyplot(fig1)

    # Residual Plot
    with col2:
        st.write("#### 🔄 Residuals Plot")
        residuals = Y_test - Y_pred
        fig2, ax2 = plt.subplots()
        ax2.scatter(Y_pred, residuals, color="#1f77b4")
        ax2.axhline(y=0, color="#ff6347", linestyle="--")
        ax2.set_xlabel("Predicted Values")
        ax2.set_ylabel("Residuals")
        ax2.set_title("Residuals Plot")
        st.pyplot(fig2)

    # Display Model Results
    st.write("### ✅ Model Results")
    st.success(f"Model trained successfully! **R² Score:** {r2_score:.2f}")
    st.write(f"**Mean Absolute Error (MAE):** {mae:.2f}")
    st.write(f"**Mean Squared Error (MSE):** {mse:.2f}")
    st.write(f"**Root Mean Squared Error (RMSE):** {rmse:.2f}")

    st.write("#### 🔍 Coefficients:")
    st.write(pd.DataFrame(model.coef_, index=feature_columns, columns=["Coefficient"]))

    # User Input for Predictions
    st.write("### 🔮 Make Predictions")
    input_values = {}
    for col in feature_columns:
        input_values[col] = st.number_input(f"Enter value for {col}", value=float(X[col].mean()))

    if st.button("Predict"):
        try:
            input_data = pd.DataFrame([input_values])
            prediction = model.predict(input_data)
            st.write(f"#### 🎯 Predicted Value: **{prediction[0]:.2f}**")
        except Exception as e:
            st.error(f"Error in prediction: {e}")

else:
    st.warning("⚠️ Please select both features and target columns.")

# Apply the style on every page
if "custom_style" in st.session_state:
    st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)
