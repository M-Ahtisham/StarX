import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Copy the original processed and randomized DataFrames
df_processed = st.session_state.df_processed.copy()
df_random = st.session_state.df_randomized.copy()

# Title
st.title("Predictions on Augmented Data")

# Add a slider to select the percentage of fake data
fake_data_percentage = st.slider(
    "Select the percentage of fake/random data to include:",
    min_value=25,
    max_value=50,
    value=25,  # Default value
    step=1,
    format="%d%%"
)

# Calculate the number of fake rows based on the percentage
num_fake_rows = int(len(df_processed) * (fake_data_percentage / 100))

# Select the required number of rows from the random DataFrame
df_fake = df_random.sample(n=num_fake_rows, random_state=42)

# Create the augmented DataFrame
df_augmented = pd.concat([df_processed, df_fake]).reset_index(drop=True)

# Display the augmented DataFrame
st.write("## Augmented DataFrame:")
st.dataframe(df_augmented)
st.write(" This is a dataframe that contains both the original data, and fake data added to it's end.")

# Shuffle the rows

# Store the sugmented data in the session

st.session_state.df_augmented = df_augmented



#################################### This is the code copied from pages/07_Model_Training.py ######################################


# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Mapping for Fuel Types
fuel_type_mapping = {
    1: "Petrol",
    2: "Diesel",
    3: "CNG",
    4: "Electric",
    5: "Petrol + CNG",
    6: "LPG",
    7: "Hybrid"
}
reverse_fuel_type_mapping = {v: k for k, v in fuel_type_mapping.items()}

# Mapping for Owner Types
owner_mapping = {
    "1st Owner": 1,
    "2nd Owner": 2,
    "3rd Owner": 3
}
reverse_owner_mapping = {v: k for k, v in owner_mapping.items()}

# Mapping for Companies
company_mapping = {
    "Maruti": 1,
    "Hyundai": 2,
    "Honda": 3,
    "Ford": 4,
    "Tata": 5,
    "Renault": 6,
    "Mahindra": 7,
    "Toyota": 8,
    "MG": 9,
    "Volkswagen": 10,
    "Jeep": 11,
    "Kia": 12,
    "BMW": 13,
    "Skoda": 14,
    "Nissan": 15,
    "Audi": 16,
    "Datsun": 17,
    "Mercedes": 18,
    "Fiat": 19,
    "Volvo": 20,
    "Jaguar": 21,
    "SsangYong": 22,
    "Land Rover": 23,
    "Porsche": 24
}
reverse_company_mapping = {v: k for k, v in company_mapping.items()}

# Load the DataFrame from session state
df_augmented = st.session_state.df_augmented.copy()

# Ensure proper data types and map descriptive names
df_augmented['Fuel_type'] = df_augmented['Fuel_type'].astype(int)
df_augmented['Fuel_type_label'] = df_augmented['Fuel_type'].map(fuel_type_mapping)
df_augmented['Owner'] = df_augmented['Owner'].astype(int)
df_augmented['Owner_label'] = df_augmented['Owner'].map(reverse_owner_mapping)
df_augmented['Company_label'] = df_augmented['Company'].map(reverse_company_mapping)

# Sidebar for inputs
st.sidebar.header("Input Features")
year = st.sidebar.slider("Year", int(df_augmented["Year"].min()), int(df_augmented["Year"].max()), 2017)
location = st.sidebar.selectbox("Location", sorted(df_augmented["Location"].unique()))
company_label = st.sidebar.selectbox("Company", list(company_mapping.keys()))
fuel_type_label = st.sidebar.radio("Fuel Type", list(fuel_type_mapping.values()), index=0)
kms_driven = st.sidebar.slider("Kms Driven", int(df_augmented["Kms_driven"].min()), int(df_augmented["Kms_driven"].max()), 40000)
owner_label = st.sidebar.radio("Owner Type", sorted(owner_mapping.keys()), index=0)

# Convert selected fuel type, owner type, and company back to numeric values
fuel_type = reverse_fuel_type_mapping[fuel_type_label]
owner = owner_mapping[owner_label]
company = company_mapping[company_label]

# Display input features in the main page
st.header("\U0001F527 Adjusting Input Features")
col1, col2 = st.columns(2)
with col1:
    st.write("### Selected Features")
    st.write(f"- **Year:** {year}")
    st.write(f"- **Location:** {location}")
    st.write(f"- **Company:** {company_label}")
    st.write(f"- **Fuel Type:** {fuel_type_label}")
    st.write(f"- **Kms Driven:** {kms_driven}")
    st.write(f"- **Owner Type:** {owner_label}")

st.write("### Test-Training data")
test_train_split = st.slider(
    "Select the percentage of test data",
    min_value=10,
    max_value=50,
    value=20,  # Default value
    step=1,
    format="%d%%"
)
# Prepare data for prediction
X = pd.get_dummies(df_augmented[["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"]], drop_first=True)
y = df_augmented["Price"]

# Train-test split (60% train, 40% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_train_split/100, random_state=42)

# Reindex the input data to match columns in X
input_data = pd.DataFrame([[location, kms_driven, fuel_type, owner, year, company]], 
                          columns=["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"])
input_data = pd.get_dummies(input_data, drop_first=True).reindex(columns=X.columns, fill_value=0)

# Lasso Regression
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_pred = lasso_model.predict(X_test)
lasso_mse = mean_squared_error(y_test, lasso_pred)
lasso_pred_input = lasso_model.predict(input_data)[0]

# Ridge Regression
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_pred = ridge_model.predict(X_test)
ridge_mse = mean_squared_error(y_test, ridge_pred)
ridge_pred_input = ridge_model.predict(input_data)[0]

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_pred = linear_model.predict(X_test)
linear_mse = mean_squared_error(y_test, linear_pred)
linear_pred_input = linear_model.predict(input_data)[0]



# Display predictions
with col2:
    st.write("### Prediction Results")
    st.success(f"Predicted Price (Lasso): ₹{lasso_pred_input:,.2f}")
    st.info(f"Predicted Price (Ridge): ₹{ridge_pred_input:,.2f}")
    st.warning(f"Predicted Price (Linear): ₹{linear_pred_input:,.2f}")

# Model performance metrics
st.header("\U0001F4CA Model Performance")
col3, col4 = st.columns(2)
with col3:
    st.metric("Lasso Regression MSE", f"{lasso_mse:.2f}")
    st.metric("Ridge Regression MSE", f"{ridge_mse:.2f}")
    st.metric("Linear Regression MSE", f"{linear_mse:.2f}")
with col4:
    st.warning(f" Ridge Regression MSE : {ridge_mse:.2f}, Ridge Regression has the lowest MSE, indicating it fits the data slightly better than Lasso and Linear Regression.")

    st.metric("Training Samples", f"{len(X_train)}")
    st.metric("Test Samples", f"{len(X_test)}")
    

# Visualization: Kms Driven vs. Price with Predictions Highlighted
st.header("\U0001F4C8 Data Insights")
st.subheader("Kms Driven vs. Price")

fig, ax = plt.subplots(figsize=(8, 6))

# Scatter plot using X_test and y_test
sns.scatterplot(
    x=X_test['Kms_driven'],  # Assuming 'Kms_driven' is a column in X_test
    y=y_test,                # The target variable from the test set
    ax=ax
)

# Highlight the predicted price for Lasso and Ridge
# ax.scatter(
#     [kms_driven],           # Example kms_driven value
#     [lasso_pred_input],     # Lasso prediction for the specific input
#     color="yellow",
#     s=50,
#     label="Lasso Predicted Price"
# )
ax.scatter(
    [kms_driven],           # Example kms_driven value
    [ridge_pred_input],     # Ridge prediction for the specific input
    color="red",
    s=60,
    # label="Ridge Predicted Price"
)
# ax.scatter(
#     [kms_driven],           # Example kms_driven value
#     [linear_pred_input],     # Ridge prediction for the specific input
#     color="red",
#     s=50,
#     label="Linear Predicted Price"
# )

# Add labels and title
ax.set_title("Kms Driven vs. Price (Test Data) with Predictions Highlighted")
ax.set_xlabel("Kms Driven")
ax.set_ylabel("Price (₹)")
ax.legend()

# Display the plot
st.pyplot(fig)

