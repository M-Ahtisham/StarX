import streamlit as st

class Chatbot:
    def __init__(self):
        self.state = "default"
        self.chat_history = {}  # Stores chat history
        self.message_counter = 1
        self.responses = {
            "default": {
                "greetings": [
                    "hello", "hi", "hey", "good morning", "good evening", "good afternoon",
                    "howdy", "hallo", "what's up", "sup", "hi there", "greetings",
                    "good day", "morning", "evening", "afternoon", "thanks", "thank you", 
                    "thanks a lot", "thank you so much", "much appreciated", 
                    "thankful", "cheers", "ty", "thx", "thanks a ton", "thanks so much"
                ],
                "responses": {
                    "hello": "Hi there! How can I assist you today?",
                    "hi": "Hello! What can I do for you?",
                    "hey": "Hey! How's it going? How can I help?",
                    "good morning": "Good morning! Hope you're having a great start to your day. How can I assist?",
                    "good evening": "Good evening! What can I do for you tonight?",
                    "good afternoon": "Good afternoon! How can I be of service?",
                    "howdy": "Howdy! What brings you here today?",
                    "hallo": "Hallo! Wie kann ich Ihnen helfen",
                    "what's up": "Not much, just here to help you out! What's up with you?",
                    "sup": "Sup! What do you need help with?",
                    "hi there": "Hi there! How can I make your day easier?",
                    "greetings": "Greetings! How can I be of assistance?",
                    "good day": "Good day! How can I help you today?",
                    "morning": "Morning! What can I assist you with?",
                    "evening": "Evening! How can I be of service?",
                    "afternoon": "Afternoon! Need any help?",
                    "thanks": "You're welcome! Let me know if there's anything else I can help you with.",
                    "thank you": "You're very welcome! Happy to help.",
                    "thanks a lot": "No problem at all! Glad I could assist.",
                    "thank you so much": "You're most welcome! Let me know if you need more help.",
                    "much appreciated": "Anytime! I'm here to help.",
                    "thankful": "You're welcome! Always happy to assist.",
                    "cheers": "Cheers! Let me know if there's anything else I can do.",
                    "ty": "You're welcome!",
                    "thx": "No problem! Let me know if you need anything else.",
                    "thanks a ton": "You're welcome! Glad I could help.",
                    "thanks so much": "You're welcome! Feel free to ask if you need anything else."
                },
                "fallback": "I'm not sure I understand that. Could you rephrase? Or ask something else!"
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
                response = "Sure, I can help you buy a car! Let's get started. What is your name?"
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


import streamlit as st

# Chat history dictionary (example data)
chat_history = {
    "1. You": "hallo",
    "2. Bot": "Hallo!, Wie kann ich Ihnen helfen",
    "3. You": "hiads",
    "4. Bot": "Hello! What can I do for you?"
}

# Streamlit App
st.title("Chatbot for StarX")

# Instantiate Chatbot
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()

# App container styling
st.markdown(
    """
    <style>
    .app-container {
        max-width: 400px;
        margin: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: var(--background-color);
    }
    .message {
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 70%;
    }
    .user {
        background-color: #0084ff;
        color: white;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #f1f0f0;
        color: black;
        text-align: left;
        margin-right: auto;
    }
    @media (prefers-color-scheme: dark) {
        .bot {
            background-color: #333;
            color: white;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display chat messages dynamically
st.markdown("### Chat History")
for key, message in st.session_state.bot.chat_history.items():
    if "You" in key:
        st.markdown(
            f"""
            <div class="message user">{message}</div>
            """,
            unsafe_allow_html=True
        )
    elif "Bot" in key:
        st.markdown(
            f"""
            <div class="message bot">{message}</div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break (empty space)

# Input and Buttons
col1, col2, col3 = st.columns([1, 5, 1])

# Image
with col1:
    st.image("imgs/chatbot.png", width=60)

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

# Expandable FAQ section
with st.expander("**FAQs and Tips**"):
    st.markdown(
        """
        - **What can I ask?**: - You can ask about buying a car.
        - **Can the chatbot handle greetings?**: Yes! Try saying "Hi", "Hello", or "Thank you".
        - **Want to reset the chat?**: Use the "Start a New Chat" button above.
        """
    )
