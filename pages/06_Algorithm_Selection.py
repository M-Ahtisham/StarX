import streamlit as st
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the DataFrame from session state
if "df_processed" in st.session_state:
    df_processed = st.session_state.df_processed.copy()
else:
    st.error("No data found in session state. Please upload and process data first.")
    st.stop()

# Page Header
st.title("📊 Regression Algorithm Comparison")

# Select columns for regression
st.write("### 🔧 Select Features and Target for Regression")
feature_columns = st.multiselect("📌 Select feature columns (X)", options=df_processed.columns)
target_column = st.selectbox("🎯 Select target column (Y)", options=df_processed.columns)

if feature_columns and target_column:
    # Prepare the data
    X = df_processed[feature_columns]
    Y = df_processed[target_column]

    # Train-test split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # --- Linear Regression ---
    st.subheader("📈 Linear Regression")
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    Y_pred = regr.predict(X_test)

    # Calculate metrics
    r2 = r2_score(Y_test, Y_pred)
    mae = mean_absolute_error(Y_test, Y_pred)
    rmse = mean_squared_error(Y_test, Y_pred, squared=False)
    cross_val = cross_val_score(regr, X, Y, cv=5)

    # Display results
    st.success("✅ The Linear Regression model is trained!")
    st.write(f"**Y_pred:** {Y_pred[0]}")
    st.write(f"**Linear Regression Score:** {r2:.4f}")
    st.write(f"**Linear Regression Cross-Validation Scores:** {cross_val}")

    # --- Lasso Regression ---
    st.subheader("📉 Lasso Regression")
    alpha = st.slider("🎛 Select alpha for Lasso Regression", 0.01, 1.0, step=0.01, value=0.1)
    regr_lasso = linear_model.Lasso(alpha=alpha)
    regr_lasso.fit(X_train, Y_train)
    Y_pred_lasso = regr_lasso.predict(X_test)

    # Calculate metrics
    r2_lasso = r2_score(Y_test, Y_pred_lasso)
    mae_lasso = mean_absolute_error(Y_test, Y_pred_lasso)
    rmse_lasso = mean_squared_error(Y_test, Y_pred_lasso, squared=False)
    cross_val_lasso = cross_val_score(regr_lasso, X, Y, cv=5)

    # Display results
    st.success("✅ The Lasso model is trained!")
    st.write(f"**Y_pred2:** {Y_pred_lasso[0]}")
    st.write(f"**Lasso Score:** {r2_lasso:.4f}")
    st.write(f"**Lasso Cross-Validation Scores:** {cross_val_lasso}")

    # --- Comparison Section ---
    st.subheader("🔍 Comparison of Algorithms")

    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame({
        "Metric": ["R² Score", "Mean Absolute Error (MAE)", "Root Mean Squared Error (RMSE)"],
        "Linear Regression": [r2, mae, rmse],
        "Lasso Regression": [r2_lasso, mae_lasso, rmse_lasso]
    })

    # Display comparison table
    st.write(comparison_df)

    # Determine the best algorithm
    best_algorithm = "Linear Regression" if r2 > r2_lasso else "Lasso Regression"
    st.success(f"🏆 Based on the R² Score, the best algorithm for your dataset is: **{best_algorithm}**")

else:
    st.warning("⚠️ Please select both feature columns (X) and a target column (Y).")
