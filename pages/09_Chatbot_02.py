import streamlit as st
import time

# Apply the style on every page
st.markdown(st.session_state["custom_style"], unsafe_allow_html=True)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to reset the chat
def reset_chat():
    st.session_state.chat_history = []
    st.rerun()  # Updated to use st.rerun()

# Title and header
st.title("🏎️ Car Insights Chatbot")
st.subheader("Ask me anything about cars in India!")
st.markdown("---")

# Load the DataFrame from session state
df_processed = st.session_state.df_processed.copy()

# Button to start a new chat
if st.button("🗑️ Start a New Chat"):
    reset_chat()

# Display chat history in bubbles
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style="background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: right; clear: both;">
                <strong>You:</strong> {message['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif message["role"] == "bot":
        st.markdown(
            f"""
            <div style="background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: left; clear: both;">
                <strong>Bot:</strong> {message['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# Input box for user query
user_input = st.text_input("Type your message here 👇", key="user_input")

# Quick reply buttons
st.markdown("Quick Replies:")
cols = st.columns([1, 1, 1, 1, 1])
if cols[0].button("Tell me car prices"):
    user_input = "Tell me car prices"
if cols[1].button("Latest car models"):
    user_input = "Latest car models"
if cols[2].button("Fuel types"):
    user_input = "Fuel types"
if cols[3].button("Thank you"):
    user_input = "Thank you"
if cols[4].button("Goodbye"):
    user_input = "Goodbye"

if user_input:
    # Add a typing animation for bot response
    with st.spinner("Bot is typing..."):
        time.sleep(1.5)  # Simulates typing delay

    # Bot response logic
    if user_input.lower() in ["hi", "hello", "hey"]:
        bot_response = "Hello! How can I assist you today?"
    elif user_input.lower() in ["bye", "goodbye"]:
        bot_response = "Goodbye! Have a great day!"
    elif user_input.lower() == "thank you":
        bot_response = "You're welcome!"
    elif user_input.lower() == "tell me car prices":
        bot_response = "Car prices in India range from ₹2.5 lakhs to over ₹1 crore depending on the model and brand."
    elif user_input.lower() == "latest car models":
        bot_response = "The latest car models include Hyundai Exter, Tata Nexon EV, and Maruti Jimny."
    elif user_input.lower() == "fuel types":
        bot_response = "Cars are available in petrol, diesel, electric, and CNG fuel types."
    else:
        bot_response = f"Sorry, I don't have an answer for '{user_input}' yet. Ask me something else!"

    # Save the conversation
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_response})

    # Display the bot response
    st.markdown(
        f"""
        <div style="background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: left; clear: both;">
            <strong>Bot:</strong> {bot_response}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Expandable FAQ section
with st.expander("FAQs and Tips"):
    st.write(
        """
        - **What can I ask?**: You can ask about car prices, fuel types, latest models, and more.
        - **Can the chatbot handle greetings?**: Yes! Try saying "Hi", "Hello", or "Thank you".
        - **Want to reset the chat?**: Use the "Start a New Chat" button above.
        """
    )
