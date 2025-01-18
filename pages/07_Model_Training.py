import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the DataFrame from session state
df_processed = st.session_state.df_processed.copy()

# Ensure proper data types
df_processed['Fuel_type'] = df_processed['Fuel_type'].astype(int)
df_processed['Owner'] = df_processed['Owner'].astype(int)

# Title and description
st.title("🚗 Car Price Prediction")
st.write("This application predicts car prices based on various factors and provides insights into the dataset.")

# Sidebar for inputs
st.sidebar.header("Input Features")
year = st.sidebar.slider("Year", int(df_processed["Year"].min()), int(df_processed["Year"].max()), 2017)
location = st.sidebar.selectbox("Location", df_processed["Location"].unique())
company = st.sidebar.selectbox("Company", df_processed["Company"].unique())
fuel_type = st.sidebar.radio("Fuel Type", sorted(df_processed["Fuel_type"].unique()), index=0)
kms_driven = st.sidebar.slider("Kms Driven", int(df_processed["Kms_driven"].min()), int(df_processed["Kms_driven"].max()), 40000)
owner = st.sidebar.radio("Owner Type", sorted(df_processed["Owner"].unique()), index=0)

# Display input features in the main page
st.header("🔧 Adjust Input Features")
col1, col2 = st.columns(2)
with col1:
    st.write("### Selected Features")
    st.write(f"- **Year:** {year}")
    st.write(f"- **Location:** {location}")
    st.write(f"- **Company:** {company}")
    st.write(f"- **Fuel Type:** {fuel_type}")
    st.write(f"- **Kms Driven:** {kms_driven}")
    st.write(f"- **Owner Type:** {owner}")

# Prepare data for prediction
X = df_processed[["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"]]
y = df_processed["Price"]

# Train-test split and model training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the input data
input_data = pd.DataFrame([[location, kms_driven, fuel_type, owner, year, company]], 
                          columns=["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"])
prediction = model.predict(input_data)[0]

# Display prediction
with col2:
    st.write("### Prediction Results")
    st.success(f"Predicted Price: ₹{prediction:,.2f}")

# Model performance metrics
y_pred_test = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred_test)

st.header("📊 Model Performance")
col3, col4 = st.columns(2)
with col3:
    st.metric("Mean Squared Error (MSE)", f"{mse:.2f}")
    st.write("This metric indicates how well the model is performing.")
with col4:
    st.metric("Training Samples", f"{len(X_train)}")
    st.metric("Test Samples", f"{len(X_test)}")

# Visualization: Price distribution by year
st.header("📈 Data Insights")
st.subheader("Price Distribution by Year")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_processed, x="Year", y="Price", palette="coolwarm", ax=ax)
plt.title("Car Price Distribution by Year")
plt.xlabel("Year")
plt.ylabel("Price (₹)")
st.pyplot(fig)

# Visualization: Scatterplot of Kms Driven vs. Price
st.subheader("Kms Driven vs. Price")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_processed, x="Kms_driven", y="Price", hue="Fuel_type", palette="viridis", ax=ax)
plt.title("Kms Driven vs. Price with Fuel Type")
plt.xlabel("Kms Driven")
plt.ylabel("Price (₹)")
plt.legend(title="Fuel Type", loc="upper right")
st.pyplot(fig)
