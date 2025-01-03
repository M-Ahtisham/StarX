import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize chatbot context in session state
if "context" not in st.session_state:
    st.session_state.context = {}

# File upload section
st.title("Interactive Chatbot for Dataset Exploration")
st.subheader("Original Dataset")
uploaded_file = 'data/Quikr_car.csv'

# Load dataset and store it in session state
if uploaded_file or isinstance(uploaded_file, str):  # Support both file uploads and file paths
    try:
        # Load dataset based on file type or hardcoded file path
        if isinstance(uploaded_file, str):  # When a file path is directly provided
            if uploaded_file.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.endswith('.json'):
                df = pd.read_json(uploaded_file)
        else:  # When a file is uploaded through Streamlit
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
        
        # Store dataset in context
        st.session_state.context['dataset'] = df
        st.session_state.context['columns'] = df.columns.tolist()
        st.session_state.context['row_count'] = df.shape[0]
        st.session_state.context['data_preview'] = df.head().to_dict()
        
        # Display the uploaded dataset
        st.subheader("Uploaded Dataset")
        st.dataframe(df)

        # Provide dataset summary
        st.write(f"### Dataset Summary")
        st.write(f"- **Number of rows:** {df.shape[0]}")
        st.write(f"- **Number of columns:** {df.shape[1]}")
        st.write(f"- **Columns:** {', '.join(df.columns)}")

    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
else:
    st.info("Please upload a dataset to proceed.")

# Chatbot response function
def chatbot_response(query):
    """
    Provides intelligent responses based on user queries and uploaded dataset.
    """
    context = st.session_state.context

    if "dataset" not in context:
        return "No dataset loaded. Please upload a dataset first."

    # Handle queries related to dataset structure
    if "columns" in query.lower():
        return f"The dataset contains the following columns: {', '.join(context['columns'])}."
    
    if "row count" in query.lower() or "size" in query.lower():
        return f"The dataset has {context['row_count']} rows."

    if "preview" in query.lower() or "first rows" in query.lower():
        return f"Here is a preview of the dataset:\n{pd.DataFrame(context['data_preview'])}"

    # Handle queries related to visualization
    if "visualize" in query.lower() or "scatter" in query.lower():
        if "columns" in context:
            return f"Available columns for visualization: {', '.join(context['columns'])}."
        else:
            return "No columns available for visualization. Please upload a dataset."

    # Default response for unsupported queries
    return "I'm sorry, I couldn't understand your question. Please ask about the dataset structure, size, preview, or visualizations."

# Chatbot interaction section
st.header("Ask the Chatbot")
user_query = st.text_input("Ask a question about your dataset (e.g., 'What are the columns?', 'Visualize data').")

if user_query:
    response = chatbot_response(user_query)
    st.write(f"Chatbot: {response}")

# Scatter plot visualization if requested by the user
if "visualize" in user_query.lower() and "dataset" in st.session_state.context:
    st.subheader("Scatter Plot Visualization")

    # User selects columns for scatter plot
    x_axis = st.selectbox("Select X-axis for the scatter plot", options=st.session_state.context['columns'])
    y_axis = st.selectbox("Select Y-axis for the scatter plot", options=st.session_state.context['columns'])

    # Display scatter plot
    if x_axis and y_axis:
        st.write(f"### Scatter Plot: {x_axis} vs {y_axis}")
        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis], alpha=0.7, color="blue")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{x_axis} vs {y_axis}")
        st.pyplot(fig)

# Download section for processed dataset
if "dataset" in st.session_state.context:
    st.subheader("Download Processed Dataset")
    processed_csv = st.session_state.context['dataset'].to_csv(index=False).encode('utf-8')
    st.download_button("Download Dataset as CSV", data=processed_csv, file_name="processed_dataset.csv", mime="text/csv")


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
