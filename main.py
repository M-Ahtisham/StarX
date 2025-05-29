import streamlit as st
import pandas as pd



st.title("StarX")
st.image("imgs/star_x.webp")



st.markdown("""
This app provides insights into car prices in India based on a dataset containing details like location, year, kilometers driven, fuel type, and ownership.

You can explore the data and get insights such as:
- **Average car prices** by location and brand.
- **The impact of kilometers driven and fuel type** on car pricing.
- **Recommendations for pricing** based on user inputs.

## Dataset Overview

The dataset contains the following columns:
- **Name**: The name and model of the car.
- **Label**: Category of the car (e.g., Platinum).
- **Location**: The city where the car is located.
- **Price**: The price of the car in Indian Rupees.
- **Kms_driven**: The distance the car has traveled.
- **Fuel_type**: The type of fuel the car uses (Petrol/Diesel).
- **Owner**: Ownership history of the car.
- **Year**: The year the car was manufactured.
- **Company**: The manufacturer of the car.
""")


st.sidebar.success("Select the menu points to navigate through the features.")

# Adding interactivity (future sections to be implemented)
st.markdown("## Future Features")
st.write("This app will be extended to include:")
st.write("- Data visualization for trends in car pricing.")
st.write("- Machine Learning-based price prediction for new listings.")
st.write("- Filters to customize data views.")

# Placeholder for data loading section
st.markdown("## Data Acquisition")
st.write("'Data acquisition', i.e., loading the dataset, will be implemented in this script.")

# Load the CSV file into a DataFrame
file_path = 'data/Quikr_car.csv' 
df = pd.read_csv(file_path)

# This stores the data frame in the session state
st.session_state.original_df = df


#This is a Custom Styling
CUSTOM_STYLE = """
    <style>
    :root {
        --primary-color: #1a73e8;          /* Vibrant blue for highlights */
        --secondary-color: #f1f3f4;       /* Light gray for background */
        --text-color: #202124;            /* Standard text color */
        --border-radius: 12px;            /* Smooth rounded corners */
        --shadow-color: rgba(26, 115, 232, 0.3); /* Soft blue shadow */
    }

    [data-testid="stSidebarContent"] {
        color: var(--text-color);          /* Sidebar text color */
        background-color: var(--secondary-color); /* Sidebar background color */
        font-family: 'Roboto', sans-serif; /* Modern font */
        padding: 20px;                     /* Adds spacious padding */
        border-radius: var(--border-radius); /* Rounded corners */
        border: 2px solid var(--primary-color); /* Highlight border */
        box-shadow: 0px 4px 12px var(--shadow-color); /* Subtle shadow effect */
    }

    /* Hover effect for sidebar links */
    [data-testid="stSidebarContent"] a:hover {
        color: var(--primary-color);       /* Highlight color on hover */
        text-decoration: underline;       /* Add underline on hover */
    }

    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #4a90e2;      /* Softer blue for dark mode */
            --secondary-color: #1e1e1e;   /* Darker background */
            --text-color: #f5f5f5;        /* Lighter text for dark mode */
            --shadow-color: rgba(74, 144, 226, 0.3); /* Softer shadow for dark mode */
        }

        [data-testid="stSidebarContent"] {
            color: var(--text-color);      /* Text color in dark mode */
            background-color: var(--secondary-color); /* Background in dark mode */
            border-color: var(--primary-color); /* Border matches primary color */
        }
    }
    
    </style>
    """


# We store it in the session state
if "custom_style" not in st.session_state:
    st.session_state["custom_style"] = CUSTOM_STYLE

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)


