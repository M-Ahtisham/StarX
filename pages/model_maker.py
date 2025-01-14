# Import necessary libraries
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pickle
import os

# ✅ Ensure correct file path
# Check the current working directory
print("Current Working Directory:", os.getcwd())

# ✅ Use the correct path to your dataset
file_path = "/Users/love/Desktop/StarX/preprocessed.csv"
df = pd.read_csv(file_path)

# Drop the unnecessary index column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Prepare features (X) and target (Y)
X = df.drop(columns=["Price"])
Y = df["Price"]

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# ✅ Train the Lasso Regression model
lasso_model = Lasso(alpha=1.0)
lasso_model.fit(X_train, Y_train)

# ✅ Make predictions on the test set
Y_pred = lasso_model.predict(X_test)

# ✅ Evaluate the model
mae = mean_absolute_error(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(Y_test, Y_pred)

# Print evaluation metrics
print("Model Evaluation Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

# ✅ Save the model as a .pkl file
model_filename = "/Users/love/Desktop/StarX/lasso_model.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(lasso_model, file)

print(f"Model saved as {model_filename}")

# ✅ Load the model back for predictions
with open(model_filename, "rb") as file:
    loaded_model = pickle.load(file)

# ✅ Example prediction using the loaded model
sample_data = X_test.iloc[0:1]  # Taking the first row from the test set as a sample
sample_prediction = loaded_model.predict(sample_data)

print(f"Sample Prediction: {sample_prediction[0]:.2f}")
