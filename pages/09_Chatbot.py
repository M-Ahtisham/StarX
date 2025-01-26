import streamlit as st
import pickle
import pandas as pd



class Chatbot:
    def __init__(self):
        self.state = "default"
        self.chat_history = {}  # Stores chat history
        self.message_counter = 1
        self.responses = {
            "default": {
                "greetings": [
                    "hello", "hi", "hey", "hay", "good morning", "good evening", "good afternoon",
                    "howdy", "hallo", "servus", "what's up", "sup", "hi there", "greetings",
                    "good day", "morning", "evening", "afternoon", "thanks", "thank you", 
                    "thanks a lot", "thank you so much", "much appreciated", "bot", "help",
                    "thankful", "cheers", "thx", "thanks a ton", "thanks so much"
                ],
                "responses": {
                    "hello": "Hi there! How can I assist you today?",
                    "hi": "Hello! What can I do for you?",
                    "hey": "Hey! How's it going? How can I help?",
                    "hay": "Hey! How's it going? How can I help?",
                    "good morning": "Good morning! Hope you're having a great start to your day. How can I assist?",
                    "good evening": "Good evening! What can I do for you tonight?",
                    "good afternoon": "Good afternoon! How can I be of service?",
                    "howdy": "Howdy! What brings you here today?",
                    "hallo": "Hallo! Wie kann ich Ihnen helfen",
                    "servus": "Servus! Wia ko i Eana huifa?",
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
                    "bot": "Yep, a robot who loves helping humans. How can I assist you today?",
                    "help": "I’m here to help—just let me know what you need!",
                    "thankful": "You're welcome! Always happy to assist.",
                    "cheers": "Cheers! Let me know if there's anything else I can do.",
                    "thx": "No problem! Let me know if you need anything else.",
                    "thanks a ton": "You're welcome! Glad I could help.",
                    "thanks so much": "You're welcome! Feel free to ask if you need anything else."
                },
                "fallback": "I'm not sure I understand that. Could you rephrase? Or ask something else!"
            },
            "predict_price": {
                "prompt": "I can help predict car prices! Please provide the Kms driven, number of Owners, and Year, separated by commas.",
                "next_step": "process_car_data"
            },
            "process_car_data": {
                "prompt": "Thank you! Let me check the car prices for you.",
                "next_step": None  # End state
            },
            "best_deal": {
                "prompt": "What price range are you looking to buy cars in? Please provide a price range (e.g., 0-10000, 10000-50000).",
                "next_step": "process_best_deal"
            },
            "process_best_deal": {
                "prompt": "Let me find the best deal for you based on your price range.",
                "next_step": None  # End state
            }
        }
        
        ## This is a shortlisted dataset containing the best deals for every price range
        self.car_data = [
            {"name": "\n • Maruti Suzuki Maruti 800 Std BSII - 2005, 1,08,252 Kms driven, Price 65,000INR at Chennai", "price": 65000},
            {"name": "\n • Chevrolet Beat LT Petrol - 2010, 55,000 Kms driven, Price 1,75,000INR at Bangalore", "price": 175000},
            {"name": "\n • Toyota Corolla H5 1.8E - 2006, 80,000 Kms driven, Price 1,70,000INR at Chennai", "price": 170000},
            {"name": "\n • Ford Figo 1.5 TITANIUM - 2010, 88,000 Kms driven, Price 1,76,000INR at Chennai", "price": 176000},
            {"name": "\n • Hyundai Eon Era Plus - 2014, 65,308 Kms driven, Price 2,77,599INR at Chennai", "price": 277599},
            {"name": "\n • Hyundai Elite i20 1.2 ASTA O CVT - 2019, 37,522 Kms driven, Price 8,25,299INR at Chennai", "price": 825299},
            {"name": "\n • Hyundai Venue S MT Turbo GDI 1.0L - 2019, 1,954 Kms driven, Price 8,55,299INR at Chennai", "price": 855299},
            {"name": "\n • Maruti Suzuki Vitara Brezza VDi - 2019, 29,110 Kms driven, Price 8,38,699INR at Pune", "price": 838699},
            {"name": "\n • Tata Hexa XM 4x2 7 STR - 2018, 60,000 Kms driven, Price 12,00,000INR at Madurai", "price": 1200000},
            {"name": "\n • Maruti Suzuki Ciaz ZDi Plus SHVS RS - 2015, 12,500 Kms driven, Price 7,40,000INR at Chennai", "price": 740000},
            {"name": "\n • Audi Q7 35 TDI Premium Plus Sunroof - 2017, 65,000 Kms driven, Price 22,50,000INR at Chennai", "price": 2250000},
            {"name": "\n • Jaguar XF 2.2 Diesel Luxury - 2014, 20,000 Kms driven, Price 21,50,000INR at Mumbai", "price": 2150000},
            {"name": "\n • BMW 3 Series 320d Luxury Line - 2015, 61,000 Kms driven, Price 18,90,000INR at Mumbai", "price": 1890000},
            {"name": "\n • Kia Seltos GTX Plus 1.4 - 2020, 19,500 Kms driven, Price 18,31,000INR at Bangalore", "price": 1831000},
            {"name": "\n • Hyundai Creta - 2020, 14,506 Kms driven, Price 18,04,399INR at Pune", "price": 1804399}
        ]
        self.price_ranges = [
            (0, 10000),
            (10000, 50000),
            (50000, 100000),
            (100000, 200000),
            (200000, 500000),
            (500000, 1000000),
            (1000000, 2000000)
        ]

    def detect_keywords(self, user_input, keywords):
        return any(keyword in user_input.lower() for keyword in keywords)

    def set_state(self, state):
        self.state = state

    def add_to_history(self, sender, message):
        self.chat_history[f"{self.message_counter}. {sender}"] = message
        self.message_counter += 1

    def respond(self, user_input):
        self.add_to_history("You", user_input)

        ########### ---- Use Case 1 ----- ##########

        if self.state == "predict_price":
            response = self.responses["predict_price"]["prompt"]
            self.add_to_history("Bot", response)
            self.set_state(self.responses["predict_price"]["next_step"])
            return response
        
        ########### ---- Use Case 2 ----- #########
        elif self.state == "best_deal":
            # Ask for price range
            response = self.responses["best_deal"]["prompt"]
            self.add_to_history("Bot", response)
            self.set_state(self.responses["best_deal"]["next_step"])
            return response
        
        elif self.state == "process_best_deal":
            # Get the price range from the user input
            try:
                price_range = [int(x.strip()) for x in user_input.split("-")]
                if len(price_range) == 2:
                    min_price, max_price = price_range
                    matching_cars = self.get_matching_cars(min_price, max_price)
                    if matching_cars:
                        car_names = [car['name'] for car in matching_cars]
                        response = f"Here are some best deals in your price range: {', '.join(car_names)}."
                        self.set_state("default")  # Reset state after processing
                    else:
                        response = "Sorry, no cars match your price range. Maybe try a different price range?"
                    self.add_to_history("Bot", response)
                else:
                    response = "Please provide a valid price range (e.g., 0-10000)."
            except Exception as e:
                response = "There was an error processing your input. Please try again."
            
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
            if self.detect_keywords(user_input, ["best deal", "best offer", "great deal", "good offer", "amazing deal", "special offer"]):
                response = "I can help you find the best deal! What price range are you looking for?"
                self.set_state("best_deal")
            elif ("predict" in user_input.lower() or "estimate" in user_input.lower() or "calculate" in user_input.lower()) and "price" in user_input.lower() :
                response = "Sure, I can help you get a price predition for a car!\nLet's get started. What is your name?"
                self.set_state("predict_price")
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

    def get_matching_cars(self, min_price, max_price):
        return [car for car in self.car_data if min_price <= car["price"] <= max_price]


    def load_model(self):
        model_path = 'models/linear_model.pkl'
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        return model

    # Function to process car purchase and predict price
    def process_car_purchase(self, kms_driven, owners, year, location=2, fuel_type=1, company=16):
        model = self.load_model()
        
        try:
            # Convert inputs to appropriate types
            kms_driven = int(kms_driven.replace(",", ""))  # Remove commas and convert to int
            owners = int(owners)
            year = int(year)
            
            # Validate input values
            if kms_driven <= 0 or owners <= 0 or year < 1900 or year > 2025:
                return "Invalid input values. Please provide realistic data."
            
            # Prepare input data
            input_data = pd.DataFrame([[location, kms_driven, fuel_type, owners, year, company]],
                                    columns=["Location", "Kms_driven", "Fuel_type", "Owner", "Year", "Company"])
            
            # One-hot encode the input data and ensure it matches the model's feature names
            X = pd.get_dummies(input_data, drop_first=True)
            for col in model.feature_names_in_:
                if col not in X.columns:
                    X[col] = 0  # Add missing columns with default value
            X = X[model.feature_names_in_]
            
            # Predict the price using the loaded model
            predicted_price = model.predict(X)[0]
            
            # Sanity check for negative predictions
            if predicted_price < 0:
                return "The estimated price is invalid. Please verify your inputs or try again."
            
            return f"The estimated price for this car is ₹{predicted_price:,.2f}. "
        except Exception as e:
            return f"An error occurred during processing: {str(e)}"



# Streamlit App
st.title(" 🏎️ Chatbot for StarX")

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
        max-width: 60%;
    }
    .user {
        background-color: #0084ff;
        color: white;
        text-align: right;
        margin-left: auto;
        max-width: 50%;
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
    
    # Replace line breaks with <br> tags
    message = message.replace("\n", "<br>")
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
        - **What can I ask?**: - You can ask to get predictions of a car. Or for best deals of cars.
        - **How does it work?**: - The Chatbot uses keyword-spotting and logic to give response based on your inputs.
        - **Can the chatbot handle greetings?**: Yes! Try saying "Hi", "Hello", or "Thank you".
        - **Is it case-sensitive?**: No, you can type in any case, and the chatbot will understand.
        - **How accurate are the predictions?**: The predictions are based on a Linear Regression trained model. So, they are accurate enough.
        - **Want to reset the chat?**: Use the "Reset Chat" button above.
        """
    )
