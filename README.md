Bhatti, Muhammad Ahtisham, 22301502

-, Love, 12306406

**StarX** 

[MyGit Repository](https://mygit.th-deg.de/mb04502/StarX)

[Link to Wiki](https://mygit.th-deg.de/mb04502/StarX/-/wikis/1.-Introduction-and-Overview)

# Project Description
StarX is a data-driven application designed to analyze and provide insights into car prices in India. By leveraging a comprehensive dataset of vehicles, the project aims to help users explore trends, evaluate factors affecting car pricing, and receive personalized pricing recommendations.

# Project Installation
1. Clone the repository:  
   `git clone https://mygit.th-deg.de/mb04502/StarX`

2. Navigate to the project folder:  
   `cd starx`

3. Install dependencies:  
   `pip install -r requirements.txt`

4. Start the app:  
   `streamlit run main.py`

# Project Data
The dataset used in this project is sourced from [Kaggle](https://www.kaggle.com/datasets/abhikalpsrivastava15/quikr-cars-dataset). It contains information about used cars available for sale in India, including details such as:

- **Name**: The model name of the car.
- **Label**: The car's classification (e.g., "PLATINUM").
- **Location**: The city where the car is listed for sale.
- **Price**: The listed price of the car in Indian Rupees.
- **Kms_driven**: The total kilometers the car has been driven.
- **Fuel_type**: The type of fuel the car uses (e.g., Petrol, Diesel).
- **Owner**: The ownership status (e.g., 1st Owner, 2nd Owner).
- **Year**: The manufacturing year of the car.
- **Company**: The car manufacturer (e.g., Ford, Maruti, Hyundai).

This dataset helps analyze trends in used car pricing and identify factors that influence the price such as brand, year, fuel type, and more.

In this project, outliers in the cars dataset were identified by plotting graphs such as scatter plots to visualize values that deviate from the usual range. The rows with these outlier values, particularly in the **Price** and **Kms_driven** columns, were then removed to ensure the dataset is more accurate and representative of typical car listings.


# Basic Usage
To start the project, first ensure that all the required dependencies are installed. You can do this by running the following command:
   
   `pip install -r requirements.txt`

Once the environment is set up, you can run the project using the following command:

   `streamlit run main.py`
## Key Use Cases
- **Data Analysis**: Analyze car prices, kilometers driven, and other factors affecting the price.
- **Visualizations**: View graphical representations of the data, such as price distribution and mileage vs. price.
- **Data Cleaning**: Remove outliers based on statistical analysis and visual inspections.
- **Car Recommendation**: Recommend a car based on user input, such as budget, fuel type, and location.


# Implementation of the Requests
This describes how the code implements a request. Also it must describe, how the a student contributed to the implementation of the request.

# Right-fit question
Here we will argues about right questions to be asked to the chatbot

# Work done
It must describe, who has implemented which request and at  which time