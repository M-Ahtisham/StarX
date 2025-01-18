import streamlit as st
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
import numpy as np

# Example dataset
X = np.random.rand(100, 1) * 10
y = 3 * X.flatten() + np.random.randn(100) * 3

# Models
linear_model = LinearRegression()
lasso_model = Lasso(alpha=0.1)

# Train models
linear_model.fit(X, y)
lasso_model.fit(X, y)

# Predictions and scores
y_pred = linear_model.predict([[3]])
linear_score = linear_model.score(X, y)
linear_cv_scores = cross_val_score(linear_model, X, y, cv=5)

y_pred2 = lasso_model.predict([[3]])
lasso_score = lasso_model.score(X, y)
lasso_cv_scores = cross_val_score(lasso_model, X, y, cv=5)

# Layout for Linear Regression Feedback
st.success("✅ The Linear Regression model is trained!")
st.write(f"**Y_pred**: {y_pred[0]}")
st.write(f"**Linear regression score**: {linear_score:.3f}")
st.write(f"**Linear regression cross_val_scores**: {linear_cv_scores}")

# Layout for Lasso Feedback
st.success("✅ The Lasso model is trained!")
st.write(f"**Y_pred2**: {y_pred2[0]}")
st.write(f"**Lasso score**: {lasso_score:.3f}")
st.write(f"**Lasso cross_val_scores**: {lasso_cv_scores}")

# Adding Comparison Chart
chart_data = pd.DataFrame({
    'Model': ['Linear Regression', 'Lasso Regression'],
    'Test R²': [linear_score, lasso_score],
    'Mean CV R²': [linear_cv_scores.mean(), lasso_cv_scores.mean()]
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
    options=['Linear Regression', 'Lasso Regression']
)

st.write(f"### You selected: {selected_model}")