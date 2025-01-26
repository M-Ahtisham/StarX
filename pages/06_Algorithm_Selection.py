import streamlit as st
import pandas as pd
import altair as alt
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import cross_val_score
import numpy as np





# Check if 'original_df', 'df_transformed', and 'df_processed' exist in session state
if 'original_df' in st.session_state and 'df_transformed' in st.session_state and 'df_processed' in st.session_state:
    # Apply the style on every page
    st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

    # Load the DataFrame from session state
    df_processed = st.session_state.df_processed.copy()

    # Check and ensure that required columns exist
    required_columns = ['Price', 'Kms_driven']  # Replace with actual column names
    if not all(col in df_processed.columns for col in required_columns):
        st.error(f"The required columns {required_columns} are not in the DataFrame. Available columns: {df_processed.columns.tolist()}")
    else:
        # Extract features and target (ensure correct column names from your dataset)
        X = df_processed[['Kms_driven']].values  # Replace 'Kms_driven' with your actual feature column name
        y = df_processed['Price'].values    # Replace 'Price' with your actual target column name

        # Normalize features to highlight model differences
        X_mean = X.mean()
        X_std = X.std()
        X_normalized = (X - X_mean) / X_std

        # Models
        ridge_model = Ridge(alpha=1.0)
        lasso_model = Lasso(alpha=0.1)
        linear_model = LinearRegression()

        # Train models
        ridge_model.fit(X_normalized, y)
        lasso_model.fit(X_normalized, y)
        linear_model.fit(X_normalized, y)

        # Predictions and scores
        y_pred_ridge = ridge_model.predict(([[50000]] - X_mean) / X_std)  # Normalize input
        y_pred_lasso = lasso_model.predict(([[50000]] - X_mean) / X_std)  # Normalize input
        y_pred_linear = linear_model.predict(([[50000]] - X_mean) / X_std)  # Normalize input

        ridge_score = ridge_model.score(X_normalized, y)
        ridge_cv_scores = cross_val_score(ridge_model, X_normalized, y, cv=5)

        lasso_score = lasso_model.score(X_normalized, y)
        lasso_cv_scores = cross_val_score(lasso_model, X_normalized, y, cv=5)

        linear_score = linear_model.score(X_normalized, y)
        linear_cv_scores = cross_val_score(linear_model, X_normalized, y, cv=5)

        # Layout for Ridge Regression Feedback
        st.success("✅ The Ridge Regression model is trained!")
        st.write(f"**Y_pred (Ridge)**: {y_pred_ridge[0]}")
        st.write(f"**Ridge regression score**: {ridge_score:.3f}")
        st.write(f"**Ridge regression cross_val_scores**: {ridge_cv_scores}")

        # Layout for Lasso Feedback
        st.success("✅ The Lasso model is trained!")
        st.write(f"**Y_pred (Lasso)**: {y_pred_lasso[0]}")
        st.write(f"**Lasso score**: {lasso_score:.3f}")
        st.write(f"**Lasso cross_val_scores**: {lasso_cv_scores}")

        # Layout for Linear Regression Feedback
        st.success("✅ The Linear Regression model is trained!")
        st.write(f"**Y_pred (Linear Regression)**: {y_pred_linear[0]}")
        st.write(f"**Linear Regression score**: {linear_score:.3f}")
        st.write(f"**Linear Regression cross_val_scores**: {linear_cv_scores}")

        # Adding Comparison Chart
        chart_data = pd.DataFrame({
            'Model': ['Ridge Regression', 'Lasso Regression', 'Linear Regression'],
            'Test R²': [ridge_score, lasso_score, linear_score],
            'Mean CV R²': [ridge_cv_scores.mean(), lasso_cv_scores.mean(), linear_cv_scores.mean()]
        })

        st.markdown("### R² Scores Comparison")

        chart = alt.Chart(chart_data).transform_fold(
            ['Test R²', 'Mean CV R²'],
            as_=['Metric', 'Value']
        ).mark_bar().encode(
            x=alt.X('Model:N', title="Model"),
            y=alt.Y('Value:Q', title="R² Score"),
            color=alt.Color('Metric:N', title="Metric"),
            tooltip=['Metric:N', 'Value:Q']
        ).properties(
            width=600,
            height=400,
            title="R² Scores Comparison"
        )

        st.altair_chart(chart)

    # Adding Final Selection Option
    selected_model = st.selectbox(
        "Select your preferred model based on the scores:",
        options=['Ridge Regression']  # Restricting to Ridge Regression only
    )

    st.write(f"### You selected: {selected_model}")

else:
    # Error message if any of the dataframes is missing
    st.error("Error: The app must be started again, or the pages must be launched in the correct order.")
