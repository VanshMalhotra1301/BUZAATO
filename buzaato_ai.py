import streamlit as st
import google.generativeai as genai
import time
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from utils import typewriter_modern  # your custom function
from your_model import model, BUZAATO_CONTEXT  # placeholders for actual import
import random

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyBjHr0stcECyeRGTbs6gYJTb-QQZ6atY7Q")

# ✅ Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ BUzaato full context injected as the first message
BUZAATO_CONTEXT = """
You are BUzaato AI Assistant. Only answer questions related to the BUzaato Services project built for Bennett University. 
If someone asks anything outside BUzaato, politely say:
"I'm here to help only with BUzaato Services. 😊"

📌 Overview:
BUzaato is a Python-based food ordering system built for students at Bennett University. It allows users to browse menus from various campus outlets, place orders, get automatic discounts, and select delivery and payment methods. It simplifies the campus dining experience.

🎯 Core Features:
- Menu browsing from 6+ outlets
- Discount system with free Coke offers
- Accurate order billing with itemization
- Hostel-based delivery agent assignment
- Two payment options: Cash on Delivery or QR-code-based online payment
- Generates QR codes using the `qrcode` Python library
- Built using Python data structures (dicts, lists), conditionals, and loops

📞 BUzaato Support:
- Phone: +91-8708546799
- Email: support@buzaato.in
- Hours: 9:00 AM – 9:00 PM

🏬 Outlets and Menus:

Snapeats: Rajma Rice ₹70, Paneer Rice ₹90, Chole Bhature ₹60, Veg Thali ₹100, Dal Makhani + Roti ₹80, Aloo Puri ₹55, Mix Veg + Paratha ₹85, Curd Rice ₹60, Lassi ₹25, Gulab Jamun ₹30

Kathi House: Aloo Roll ₹40, Paneer Roll ₹60, Egg Roll ₹50, Chicken Roll ₹70, Double Egg Roll ₹60, Paneer Tikka Roll ₹75, Schezwan Veg Roll ₹65, Cheese Burst Roll ₹80, Mayo Roll ₹45, Soft Drink (Can) ₹35

Chai Ok: Masala Chai ₹20, Samosa ₹15, Chai + Samosa Combo ₹30, Adrak Chai ₹25, Elaichi Chai ₹25, Bun Maska ₹25, Vada Pav ₹30, Puff (Veg) ₹20, Kesar Chai ₹30, Choco Muffin ₹35

Quench: Cold Coffee ₹40, Mango Shake ₹50, Oreo Shake ₹60, Chocolate Shake ₹55, Strawberry Smoothie ₹70, Lemon Iced Tea ₹45, Watermelon Juice ₹40, Blue Lagoon ₹60, Virgin Mojito ₹65, Soda Shikanji ₹30

Southern Stories: Idli Sambhar ₹50, Masala Dosa ₹70, Vada ₹40, Plain Dosa ₹60, Rava Dosa ₹75, Onion Uttapam ₹70, Mini Tiffin ₹95, Filter Coffee ₹25, Medu Vada Sambhar ₹45, Lemon Rice ₹55

Maggi Point: Plain Maggi ₹30, Masala Maggi ₹40, Cheese Maggi ₹50, Paneer Maggi ₹60, Butter Maggi ₹45, Peri Peri Maggi ₹55, Tandoori Maggi ₹65, Egg Maggi ₹50, Veggie Loaded Maggi ₹60, Chilli Garlic Maggi ₹55

🏷️ Discounts:
👉 40% OFF on orders above ₹700 + Freebie: 🍕 Get a Free Cheese Garlic Bread
👉 30% OFF on orders above ₹550 + Freebie: 🥤 1.25L Coke + 🍟 Regular Fries Free
👉 25% OFF on orders above ₹400 + Freebie: 🍩 Free Dessert of the Day
👉 20% OFF on orders above ₹300 + Freebie: 🥤 Free 750ml Beverage
👉 15% OFF on orders above ₹200
👉 10% OFF on orders above ₹150

📦 Billing & Order Logic:
- Users select outlet and items; prices are added using Python dictionaries.
- Final total is calculated.
- Discounts are applied based on thresholds.
- Receipt includes items, original total, discount amount, final amount, and freebies.

🚚 Delivery System:
- Students provide hostel and room number.
- Delivery agent is auto-assigned based on hostel mapping:

    C11 → Yuvraj 📞 9xxx
    C10 → Dhruv 📞 98xx
    C9  → Aditya 📞 8xxx
    D1  → Renuka 📞 93xx
    D2  → Rashmi 📞 87xx
    C1  → Sambhav 📞 97xx

💳 Payment:
- Cash on Delivery: Basic receipt is generated.
- Online Payment: QR code is generated using Python `qrcode` library and displayed on screen. Once scanned, a success message is shown.

🔐 Technologies Used:
- Python (dictionaries, lists, tuples, functions, conditionals, loops)
- qrcode (library for payment QR code)
- Streamlit (for web interface, if deployed visually)
- Simple procedural logic for clarity and readability

🧠 Sample Questions You Can Answer:
- "What's on the menu at Maggi Point?"
- "Who delivers to C11?"
- "Do I get a discount on ₹650 order?"
- "How does BUzaato generate QR codes?"
- "How does billing work?"
- "Which outlet serves Vada Pav?"
- "How many outlets are there?"
- "Can I pay online?"
- "How does the delivery agent get assigned?"

🧩 Future Scope (optional if asked):
- Add user logins and order history
- Integrate UPI payment gateway
- Connect with real-time delivery tracking
- Build mobile app front-end with Flutter or React Native
- Admin panel for outlet updates and order management

🎓 Origin:
The BUzaato project was built as part of a Python programming assignment for BTech students of Bennett University.

You should now be able to answer any question related to outlets, items, pricing, discounts, delivery, billing, contact info, or how the system works internally.
"""


def typewriter_modern(text, delay=0.06):
    st.markdown("""
        <style>
        .tw {
            font-weight: 700;
            font-size: 28px;
            background: linear-gradient(to right, #6c63ff, #ff6584);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Segoe UI', sans-serif;
        }
        .cursor {
            display: inline-block;
            width: 8px;
            height: 28px;
            background-color: #6c63ff;
            margin-left: 4px;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%%, 100%% { opacity: 1; }
            50%% { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)

    placeholder = st.empty()
    shown = ""
    for char in text:
        shown += char
        placeholder.markdown(f"<div class='tw'>{shown}<span class='cursor'></span></div>", unsafe_allow_html=True)
        time.sleep(delay)
    placeholder.markdown(f"<div class='tw'>{shown}</div>", unsafe_allow_html=True)




def buzaato_ai_chat():
    # 🎉 Custom Animated Header
    st.markdown("""
        <h1 style="font-family: 'Segoe UI', sans-serif; font-size: 40px; color: #1f77b4;">
            🤖 <span style="color:#ff4b4b;">BUzaato</span> AI Assistant
        </h1>
        <p style="margin-top: -10px; font-size: 16px; color: #555;">
            Your smart food & service assistant – Ask anything about menus, discounts, orders or support!
        </p>
        <style>
            .stChatMessage {
                border-radius: 16px !important;
                padding: 0.75rem 1.25rem !important;
                font-size: 16px;
                line-height: 1.5;
            }
            .st-emotion-cache-1c7y2kd {
                padding: 0.5rem 1rem !important;
            }
            .chat-avatar {
                border-radius: 50%;
                height: 40px;
                width: 40px;
            }
            .css-1dp5vir {  /* removes scroll bar glow */
                scrollbar-width: thin;
                scrollbar-color: #888 transparent;
            }
        </style>
    """, unsafe_allow_html=True)
    # 🌟 Init chat session
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.chat.send_message(BUZAATO_CONTEXT)

    # 🎯 AI Assistant Profile Card
    with st.container():
        st.markdown(
            """
            <div style='background: linear-gradient(90deg, #e3f2fd, #fce4ec); padding: 15px; border-radius: 15px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1)'>
                <h3 style='margin:0;'>🤖 BUZaato AI Assistant</h3>
                <p style='margin:5px 0 0; font-size:15px;'>Need help with ordering, offers, delivery, or food combos? I'm here 24/7!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 📜 Display chat history
    for msg in st.session_state.chat.history[1:]:
        avatar = "🧑‍💼" if msg.role == "user" else "🤖"
        with st.chat_message(msg.role, avatar=avatar):
            st.markdown(msg.parts[0].text)

    # 💬 User input field
    prompt = st.chat_input("💬 Type something like 'Show me today’s best discounts'...")

    if prompt:
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(f"**You:** {prompt}")

        try:
            # ✨ AI response
            with st.spinner("🤖 Thinking..."):
                response = st.session_state.chat.send_message(prompt)

            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)

            # 💡 Smart Suggestions (Next actions)
            with st.expander("🔮 Smart Suggestions"):
                st.markdown("""
                - 🍱 *Show today's popular combos*
                - 🧾 *Track my latest order*
                - 💳 *What offers are available on Paytm?*
                - 🛍️ *Suggest the best-rated food outlet nearby*
                """)

        except Exception as e:
            st.error("❌ Gemini API Error: Something went wrong.")
            st.exception(e)

    # 🌈 Optional fun rain animation
    rain(
        emoji=random.choice(["🍕", "🍔", "🥤", "🍟"]),
        font_size=25,
        falling_speed=3,
        animation_length="infinite",
    )

    # 🧠 Contextual Tip Banner
    if prompt and "discount" in prompt.lower():
        st.markdown(
            """
            <div style='background:#fff8e1; padding: 12px; margin-top:10px; border-left: 4px solid #ffc107; border-radius:8px; font-size:14px'>
                💡 Tip: Try ordering during <b>Lunch Hours (12–3PM)</b> or <b>Dinner Hours (7–10PM)</b> for maximum savings!
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🔁 Feedback option
    st.markdown(
        """
        <div style='margin-top:20px; font-size:14px; text-align:center'>
            💬 Want to improve BUzaato AI? <a href='#' style='color:#1e88e5;'>Give Feedback</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    if __name__ == "__main__":
        buzaato_ai_chat()

