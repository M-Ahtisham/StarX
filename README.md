Bhatti, Muhammad Ahtisham, 22301502

-, Love, 12306406

**StarX** 

[MyGit Repository](https://mygit.th-deg.de/mb04502/StarX)

[Link to Wiki](https://mygit.th-deg.de/mb04502/StarX/-/wikis/home)

# Project Description
StarX is a data-driven application designed to analyze and provide clear insights into car prices in India. Using a detailed dataset covering a wide range of vehicles, it helps users understand pricing trends, identify key factors that influence car prices, and make informed decisions. The application also offers personalized pricing recommendations, ensuring users have the right information to evaluate and compare options effectively.

# Project Installation and Running

Follow these steps to set up and run the StarX application. Make sure to have the correct versions of Python and Streamlit installed.



1. Clone the repository:  
   `git clone https://mygit.th-deg.de/mb04502/StarX`

2. Navigate to the project folder:  
   `cd starx`

3. Create a virtual environment:
   - On Windows:
      `python -m venv .venv`
   - On macOS/Linux:
      `python3 -m venv .venv`

4. Activate the virtual environment:  
   - On Windows:  
     `.venv\Scripts\activate`
   - On macOS/Linux:  
     `source .venv/bin/activate`

5. Install dependencies:  
   `pip install -r requirements.txt`

6. Start the app:  
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
StarX implements the requests as follows

1. _A multi-page Web App with Streamlit (https://streamlit.io) has to be developed._
   - StarX consists of 9 pages, all pages have to be run in the correct order since they depend on the actions from the previous page


2. _For source code and documentation, a MyGit repository and Wiki has to be used._
   - MyGit repository and Wiki have been used, see links at the top of this README file.

3. _Develop and describe 3 Personas in the Wiki._
   - 3 Personas have been developed. See Wiki section Personas.

      [Link to Personas](https://mygit.th-deg.de/mb04502/StarX/-/wikis/3.-Personas)

4. _Find 5 use cases for the application._
   - 5 Use cases were described. See Wiki under section Use Cases.

      [Link to Use Cases](https://mygit.th-deg.de/mb04502/StarX/-/wikis/4.-Use-Cases)

5. _A requirements.txt file must be used to list the used Python modules, which can be used to install them._
   - A requirements.txt file is created and can be found in the root directory of the Project.

6. _A README.md file must be created with the structure described in part 01._
   - README.md has been used and it is the file open currently. It is also located in the root directory of the Project.

7. _The module venv for a virtual project environment must be used._
   - venv is used and it has been described in the 'Project Installation and running' section of this README file.

8. _A free data source must be used. You may find it for example at Kaggle, SciKit (but not the built-in
ones), or other._
   - Kaggle was used to find the dataset for this project. More information is described in the Wiki under the Data section.

      [Link to Data](https://mygit.th-deg.de/mb04502/StarX/-/wikis/2.-Data)

9. _There must be a data import (predefined format and content of CSV)._
   - Data is imported when the main.py file is run. This is then stored in a session state and then used by the other pages.

10. _The data must be analyzed in the app (e.g. with Pandas, a Jupyter notebook must not be submitted), so that an app user gets on overview (e.g. of correlations, min/max, median, …). The result must be visualized in the app._
      - The data is analysed and an overview is given to the user in Page 1 after which the Data is transformed in Page 2, then the correlations, min/max and other metrics are descibed in the Data Transformation tab. For more information see "Data Statistics" and "Data Transformation" tab after running the app. 

11. _The data must be described in a Wiki section. The description must include the feature variables, their values incl. basic statistics like min/max, transformation (if done) and a description of the target variable._
      - ❌

12. _Identify and update outliers, if some exists. Explain your approach in the data chapter of the Wiki._
      - Outlers were found in the data by plotting graphs of the Data, these were removed by Quantile-based-approach, more information is under the Data section in the Wiki.

13. _The data must be transformed so that it can be used in the app. Follow the descriptions in https://developers.google.com/machine-learning/crash-course/numerical-data and following chapters about data._
      - The None-numeric values were transformed to numeric depending on how frequent the value appeared, more information is under the Data section in the Wiki.

14. _Add 25-50% realistic fake data sets. What is the effect to the training of the model? Explain you approach for generating the fake data and its influence on the model in the data chapter of the Wiki._
      - ❌

15. _Create several input widgets (at least 3, where 2 must be different) that change some feature variables._
      - ❌

16. _At least 2 Scikit-Learn model training algorithms (e.g. from Aurélien Géron, Chapter 4) must be applied in order to predict some variable(s). Argue in the Wiki about which one is best suited for the app._
      - ❌

17. _Select at least two use cases for which the “right fit” question for chatbots has a positive answer. Argue about why using a chatbot for the feature makes sense and write this in the Wiki._
      - ❌

18. _Create a system persona for the chatbot and document it in the Wiki._
      - ❌

19. _Create at least 3 sample dialogs for each use case you select for the chatbot. Document them in the Wiki._
      - ❌

20. _Create a high-level (dialog) flow for the use cases. Also document it in the Wiki._
      - ❌

21. _Create a rasa chat bot that must be included for the use cases. Add the source files to the MyGit repository._
      - ❌

22. _Create a video/screencast of your project. The video must show at least 3 use cases, one of them with the rasa chatbot. The video must be uploaded to the MyGit repository._
      - ❌


# Work done
It must describe, who has implemented which request and at  which time