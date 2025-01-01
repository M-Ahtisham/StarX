import streamlit as st

#This is a Custom Styling
st.markdown(
    """
    <style>
    :root {
        --sidebar-text-color: #000000;      /* Default text color for light mode */
        --sidebar-bg-color: #e8edf1;       /* Default background color for light mode */
        --sidebar-highlight-color: #d6e4f5; /* Light blue tint for light mode */
    }

    [data-testid="stSidebarContent"] {
        color: var(--sidebar-text-color);  /* Dynamic Sidebar text color */
        background-color: var(--sidebar-bg-color);  /* Dynamic Sidebar background */
        font-family: 'Arial', sans-serif;  /* Stylish font */
        padding: 15px;  /* Adds some padding */
        border-radius: 10px;  /* Smooth corner style */
        border: 2px solid var(--sidebar-highlight-color); /* Blue highlight border */
        box-shadow: 0px 4px 8px var(--sidebar-highlight-color); /* Blue shadow effect */
    }

    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        :root {
            --sidebar-text-color: #ffffff;  /* Text color for dark mode */
            --sidebar-bg-color: #333333;   /* Background color for dark mode */
            --sidebar-highlight-color: #4a90e2; /* Dark blue tint for dark mode */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("# StarX")

st.write("This app provides insights into car prices in India based on a dataset containing details like location, year, kilometers driven, fuel type, and ownership.")

st.write("You can explore the data and get insights such as:")
st.write("- Average car prices by location and brand.")
st.write("- The impact of kilometers driven and fuel type on car pricing.")
st.write("- Recommendations for pricing based on user inputs.")

st.markdown("## Dataset Overview")

st.write("The dataset contains the following columns:")
st.write("- **Name**: The name and model of the car.")
st.write("- **Label**: Category of the car (e.g., Platinum).")
st.write("- **Location**: The city where the car is located.")
st.write("- **Price**: The price of the car in Indian Rupees.")
st.write("- **Kms_driven**: The distance the car has traveled.")
st.write("- **Fuel_type**: The type of fuel the car uses (Petrol/Diesel).")
st.write("- **Owner**: Ownership history of the car.")
st.write("- **Year**: The year the car was manufactured.")
st.write("- **Company**: The manufacturer of the car.")

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

st.sidebar.success("Select the menu points from top to bottom in order to use the ML pipeline.")




