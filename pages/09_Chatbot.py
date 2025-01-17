import streamlit as st

class Chatbot:
    def __init__(self):
        self.state = "default"
        self.chat_history = {}  # Stores chat history
        self.message_counter = 1
        self.responses = {
            "default": {
                "greetings": ["hello", "hi", "good morning", "good evening", "good afternoon"],
                "responses": {
                    "hello": "Hi there! How can I help you today?",
                    "hi": "Hello! What can I do for you?",
                    "hey": "Hey! How can I help you?",
                    "good morning": "Good morning! How can I assist you?",
                    "good evening": "Good evening! How can I help?",
                    "good afternoon": "Good afternoon! What can I do for you?",
                },
                "fallback": "I'm not sure I understand that. Could you rephrase?"
            },
            "buy_car": {
                "prompt": "I can help you buy a car! Please provide the Kms driven, number of Owners, and Year, separated by commas.",
                "next_step": "process_car_data"
            },
            "process_car_data": {
                "prompt": "Thank you! Let me process your car purchase request.",
                "next_step": None  # End state
            }
        }

    def detect_keywords(self, user_input, keywords):
        return any(keyword in user_input.lower() for keyword in keywords)

    def set_state(self, state):
        self.state = state

    def add_to_history(self, sender, message):
        self.chat_history[f"{self.message_counter}. {sender}"] = message
        self.message_counter += 1

    def respond(self, user_input):
        self.add_to_history("You", user_input)

        # Handle specific states
        if self.state == "buy_car":
            response = self.responses["buy_car"]["prompt"]
            self.add_to_history("Bot", response)
            self.set_state(self.responses["buy_car"]["next_step"])
            return response

        elif self.state == "process_car_data":
            # Process the user input for Kms_driven, Owners, and Year
            try:
                car_data = [value.strip() for value in user_input.split(",")]
                if len(car_data) == 3:
                    kms_driven, owners, year = car_data
                    response = self.process_car_purchase(kms_driven, owners, year)
                    self.add_to_history("Bot", response)
                    self.set_state("default")  # Reset state after processing
                else:
                    response = "Please provide exactly three values: Kms driven, Owners, and Year, separated by commas."
            except Exception as e:
                response = "There was an error processing your input. Please try again."
            
            return response

        # Default state
        else:
            if "buy" in user_input.lower() and "car" in user_input.lower():
                response = "Sure, I can help you buy a car! Let's get started."
                self.set_state("buy_car")
            else:
                detected = False
                for greeting in self.responses["default"]["greetings"]:
                    if greeting in user_input.lower():
                        response = self.responses["default"]["responses"][greeting]
                        detected = True
                        break
                if not detected:
                    response = self.responses["default"]["fallback"]

        self.add_to_history("Bot", response)
        return response

    # Imaginary function to process the car data
    def process_car_purchase(self, kms_driven, owners, year):
        # This is a placeholder function for processing car purchases
        return f"Processing your purchase request for a car with {kms_driven} Kms driven, {owners} owners, and year {year}."

# Streamlit App
st.title("Chatbot for StarX")

# Instantiate Chatbot
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()

# Display Chat History
st.subheader("Chat History")
if st.session_state.bot.chat_history:
    for key, message in st.session_state.bot.chat_history.items():
        st.text(f"{key}: {message}")
else:
    st.text("No messages yet. Start the conversation!")

# Input and Buttons
col1, col2, col3 = st.columns([1, 5, 1])

# Image
with col1:
    st.image("imgs/chatbot.png", width = 70)

# User Input
user_input = col2.text_input("Type your message here:", key="user_input")

# Callback function for the Send button
def send_message():
    if user_input.strip():  # Check if input is not empty
        bot_response = st.session_state.bot.respond(user_input)
        st.session_state.response = bot_response

# Callback function for the Reset button
def reset_chat():
    st.session_state.bot = Chatbot()  # Reinitialize chatbot
    st.session_state.response = ""  # Clear any response
    st.session_state.user_input = ""  # Clear input field

# Buttons
with col3:
    st.button("Send", on_click=send_message)


st.button("Reset Chat", on_click=reset_chat)

