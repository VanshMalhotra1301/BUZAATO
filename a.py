from utils import typewriter_modern  # ✅ ALREADY WORKS IN STREAMLIT

from buzaato_ai import buzaato_ai_chat
#from db import create_user, check_user, insert_order, get_orders
from datetime import datetime
import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import datetime
import base64
import streamlit as st
from PIL import Image
import datetime
import uuid
from fpdf import FPDF
import tempfile
import os
import streamlit as st
import time

from supabase import create_client, Client


st.set_page_config(page_title="BUzaato Login", layout="centered")
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

img_base64 = get_base64_image("COMPANY.jpg")

def typewriter_modern(text, delay=0.07, font_size="32px", color1="#6c63ff", color2="#ff6584"):
    st.markdown("""
        <style>
        .typewriter-text {
            font-weight: 600;
            font-size: %s;
            background: linear-gradient(to right, %s, %s);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Segoe UI', sans-serif;
        }
        .typewriter-cursor {
            display: inline-block;
            margin-left: 4px;
            width: 8px;
            height: 24px;
            background-color: %s;
            animation: blink 1s infinite;
            border-radius: 2px;
        }
        @keyframes blink {
            0%%, 50%%, 100%% { opacity: 1; }
            25%%, 75%% { opacity: 0; }
        }
        </style>
    """ % (font_size, color1, color2, color1), unsafe_allow_html=True)

    placeholder = st.empty()
    display_text = ""
    
    for char in text:
        display_text += char
        placeholder.markdown(
            f"<div class='typewriter-text'>{display_text}<span class='typewriter-cursor'></span></div>",
            unsafe_allow_html=True
        )
        time.sleep(delay)

    # Final version without the cursor
    placeholder.markdown(f"<div class='typewriter-text'>{display_text}</div>", unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(145deg, #f3f4f6, #e0eafc);
        color: #222;
        margin: 0;
        padding: 0;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .stApp {
        max-width: 100% !important;
        width: 100% !important;
        height: 100vh !important;
        margin: 0 !important;
        background: #ffffff;
        border-radius: 18px !important;
        padding: 40px 60px 60px 60px !important;
        box-shadow: 0 25px 55px rgba(108, 99, 255, 0.15);
        transition: all 0.3s ease-in-out;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stApp:hover {
        background: #f9faff;
    }

    .css-18e3th9 {
        padding: 0 !important;
        margin: 0 auto !important;
        max-width: 1000px !important;
        width: 100% !important;
        height: 100% !important;
    }

    .css-1v0mbdj.stSidebar {
        background: linear-gradient(180deg, #6c63ff, #b39ddb);
        border-radius: 0 25px 25px 0;
        box-shadow: 4px 0 30px rgba(108, 99, 255, 0.15);
        padding-top: 40px;
        height: 100vh !important;
        overflow-y: auto;
        color: #fff !important;
    }

    .css-1d391kg, .css-1lcbmhc, .css-10trblm, .css-qcqlej, .css-1c7y2kd {
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }

    .stButton>button {
        background: linear-gradient(90deg, #7b68ee, #b388ff);
        color: #fff;
        border: none;
        border-radius: 30px;
        font-weight: 800;
        font-size: 17px;
        padding: 14px 34px;
        cursor: pointer;
        box-shadow: 0 12px 28px rgba(123, 104, 238, 0.35);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #5c4bd4, #9e8dff);
        transform: translateY(-2px);
        box-shadow: 0 16px 36px rgba(92, 75, 212, 0.4);
    }

    .stSelectbox, .stTextInput, .stMultiselect, .stRadio>div>div, .stTabs>div>div {
        background: #f2f5ff;
        border-radius: 22px;
        padding: 14px 22px;
        box-shadow: 0 10px 25px rgba(108, 99, 255, 0.1);
        border: none;
        font-weight: 500;
        font-size: 16px;
        color: #3c3c3c;
        transition: all 0.25s ease-in-out;
    }

    .stSelectbox:hover, .stTextInput:hover, .stMultiselect:hover, .stRadio>div>div:hover, .stTabs>div>div:hover {
        background: #e3e8ff;
        box-shadow: 0 12px 32px rgba(108, 99, 255, 0.2);
    }

    .css-1v0mbdj, .css-1cpxqw2, .css-1d391kg, .css-ffhzg2 {
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(108, 99, 255, 0.08);
        border: none !important;
    }

    .stRadio>div>label {
        font-weight: 700;
        color: #3c3c3c;
        cursor: pointer;
        transition: color 0.3s ease;
    }

    .stRadio>div>label:hover {
        color: #6c63ff;
    }

    .main h1, .main h2, .main h3 {
        color: #2c3e50;
        font-weight: 800;
        letter-spacing: 0.06em;
        margin-bottom: 24px;
        text-transform: uppercase;
        text-shadow: 0 2px 4px rgba(108, 99, 255, 0.2);
    }

    .stInfo, .stSuccess {
        border-radius: 25px;
        padding: 18px 26px;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(108, 99, 255, 0.1);
        background: #eaf0ff;
        color: #2c3e50;
        letter-spacing: 0.02em;
    }

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #e2e5ff;
        border-radius: 25px;
    }
    ::-webkit-scrollbar-thumb {
        background: #7b68ee;
        border-radius: 25px;
        box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #5c4bd4;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- DATABASE (SIMULATED) ----------------------
users = st.session_state.setdefault("users", {})
order_history = st.session_state.setdefault("order_history", {})
current_user = st.session_state.setdefault("current_user", None)

# ---------------------- MENU DATA ----------------------
outlets = {
    "Snapeats": {
        "Rajma Rice": 70,
        "Paneer Rice": 90,
        "Chole Bhature": 60,
        "Veg Thali": 100,
        "Dal Makhani + Roti": 80,
        "Aloo Puri": 55,
        "Mix Veg + Paratha": 85,
        "Curd Rice": 60,
        "Lassi": 25,
        "Gulab Jamun": 30
    },
    "Kathi House": {
        "Aloo Roll": 40,
        "Paneer Roll": 60,
        "Egg Roll": 50,
        "Chicken Roll": 70,
        "Double Egg Roll": 60,
        "Paneer Tikka Roll": 75,
        "Schezwan Veg Roll": 65,
        "Cheese Burst Roll": 80,
        "Mayo Roll": 45,
        "Soft Drink (Can)": 35
    },
    "Chai Ok": {
        "Masala Chai": 20,
        "Samosa": 15,
        "Chai + Samosa Combo": 30,
        "Adrak Chai": 25,
        "Elaichi Chai": 25,
        "Bun Maska": 25,
        "Vada Pav": 30,
        "Puff (Veg)": 20,
        "Kesar Chai": 30,
        "Choco Muffin": 35
    },
    "Quench": {
        "Cold Coffee": 40,
        "Mango Shake": 50,
        "Oreo Shake": 60,
        "Chocolate Shake": 55,
        "Strawberry Smoothie": 70,
        "Lemon Iced Tea": 45,
        "Watermelon Juice": 40,
        "Blue Lagoon": 60,
        "Virgin Mojito": 65,
        "Soda Shikanji": 30
    },
    "Southern Stories": {
        "Idli Sambhar": 50,
        "Masala Dosa": 70,
        "Vada": 40,
        "Plain Dosa": 60,
        "Rava Dosa": 75,
        "Onion Uttapam": 70,
        "Mini Tiffin": 95,
        "Filter Coffee": 25,
        "Medu Vada Sambhar": 45,
        "Lemon Rice": 55
    },
    "Maggi Point": {
        "Plain Maggi": 30,
        "Masala Maggi": 40,
        "Cheese Maggi": 50,
        "Paneer Maggi": 60,
        "Butter Maggi": 45,
        "Peri Peri Maggi": 55,
        "Tandoori Maggi": 65,
        "Egg Maggi": 50,
        "Veggie Loaded Maggi": 60,
        "Chilli Garlic Maggi": 55
    }
}

discounts = [
    (700, 40, "🍕 Get a Free Cheese Garlic Bread"),
    (550, 30, "🥤 1.25L Coke + 🍟 Regular Fries Free"),
    (400, 25, "🍩 Free Dessert of the Day"),
    (300, 20, "🥤 Free 750ml Beverage"),
    (200, 15, ""),
    (150, 10, "")
]

agents = {
    "c11": "Yuvraj 📞 9xxx", "c9": "Aditya 📞 8xxx", "c10": "Dhruv 📞 98xx",
    "d1": "Renuka 📞 93xx", "d2": "Rashmi 📞 87xx", "c1": "Sambhav 📞 97xx"
}

# ---------------------- FUNCTIONS ----------------------
#from fpdf import FPDF
def calculate_bill(order_items, menu):
    bill = sum(menu[item] for item in order_items)
    for min_amount, discount, freebie in discounts:
        if bill >= min_amount:
            final = bill - (bill * discount / 100)
            return final, discount, freebie
    return bill, 0, ""

def generate_qr(total):
    upi_link = f"upi://pay?pa=vanshmalhotra1301@oksbi&pn=BUzaato%20Services&am={total}&cu=INR"
    qr = qrcode.make(upi_link)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    return buf

def get_agent(hostel):
    return agents.get(hostel.lower(), "❌ No delivery agent for this hostel.")

def record_order(user, outlet, items, total, discount, freebie):

    hostel = st.session_state.get("hostel", "N/A")
    agent = get_agent(hostel)

    order = {
        "user": user,
        "outlet": outlet,
        "items": ', '.join(items),
        "total": total,
        "discount": discount,
        "freebie": freebie,
        # "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Out for Delivery",  # default status
        "agent": agent,
        "eta": "20–30 mins"
    }

    if "orders" not in st.session_state:
        st.session_state.orders = []
    st.session_state.orders.append(order)
    # Generate a unique order ID (not stored, just illustrative)
    order_id = str(uuid.uuid4())[:8].upper()

    # Improved timestamp format
    timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

    # "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # type: ignore


    # Optionally log or print the order ID (for internal traceability)
    print(f"[ORDER CONFIRMED] ID: {order_id} | User: {user} | Time: {timestamp}")



def get_pending_orders(user):
    # Simulated DB list; replace with real DB queries
    orders = get_orders(user)
    pending = [order for order in orders if order.get("status", "Pending") != "Delivered"]
    return pending

def track_order(user):
    orders = get_orders(user)
    for order in reversed(orders):
        if order.get("status", "Pending") != "Delivered":
            return {
                "status": order.get("status", "Out for Delivery"),
                "agent": order.get("agent", "Not Assigned"),
                "eta": order.get("eta", "20–30 mins")
            }
    return None
def get_support_info():
    return {
        "phone": "+91-8708546799",
        "email": "support@buzaato.in",
        "hours": "9:00 AM – 9:00 PM"
    }
FAKE_USERNAME = "admin"
FAKE_PASSWORD = "pass123"



def main_app():
    st.sidebar.title("🍱 BUzaato Menu Hub")
    st.markdown("""
    <style>
    body {
        background-color: #f3f4f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
    }

    /* Heading styles */
    .main h1, .main h2, .main h3 {
        color: #2c3e50;
        font-weight: 700;
    }

    /* Sidebar panel */
    .stSidebar {
        background: linear-gradient(to bottom, #ffffff, #f0f4f8) !important;
        border-right: 1px solid #e0e0e0;
        padding-top: 1rem;
    }

    /* Sidebar text */
    .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj, .css-10trblm, .css-qcqlej, .css-1c7y2kd {
        color: #2e3b4e !important;
        font-weight: 500;
    }

    /* Button styles */
    .stButton>button {
        background: linear-gradient(90deg, #42a5f5, #66bb6a);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #66bb6a, #42a5f5);
        transform: scale(1.04);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
    }

    /* Radio label */
    .stRadio>div>label {
        font-weight: 600;
        color: #37474f;
        font-size: 16px;
    }

    /* Inline code blocks */
    code {
        background-color: #e3f2fd;
        color: #1e88e5;
        padding: 3px 8px;
        border-radius: 8px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

    # Welcome banner
    st.markdown(f"""
        <div style='
            background: linear-gradient(to right, #bbdefb, #c8e6c9);
            padding: 20px;
            border-radius: 18px;
            font-size: 22px;
            font-weight: 700;
            color: #1b5e20;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.05);'>
            👋 Welcome <span style='color:#2c3e50;'>{current_user}</span> – <i>BUzaato Services India</i>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar branding
    st.sidebar.markdown("### 🍽️ <span style='color:#2c3e50;'>BUzaato Services</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<span style='color:#455a64;'>👤 Logged in as:</span> <code>{current_user}</code>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # Logout button
    if st.sidebar.button("🔓 Logout"):
        st.session_state.current_user = None
        st.rerun()

    menu_option = st.sidebar.radio("📌 Navigate", [
            "🛒 Place Order", "📜 My Orders", "💸 Offers", 
            "📦 Pending Deliveries", "📍 Track My Order", 
            "📞 Contact Support", 
            "Chat with BUZaato AI"
        ])
    
    
    if menu_option == "🛒 Place Order":
        st.markdown("""
            <h2 style='color:#2c3e50;'>🛒 Place Your Order</h2>
            <p style='font-size:16px; color:gray;'>Select your favorite dishes and enjoy delicious meals on campus! 🍽️</p>
        """, unsafe_allow_html=True)

        outlet = st.selectbox("🏪 Select Outlet", list(outlets.keys()))
        menu = outlets[outlet]

        st.markdown("### 📋 Menu")
        with st.container():
            for item, price in menu.items():
                st.markdown(f"<li style='font-size:17px; line-height:1.8'><b>{item}</b> — ₹{price}</li>", unsafe_allow_html=True)

        order_items = st.multiselect("🍴 Choose Items", list(menu.keys()))

        if order_items:
            bill = sum(menu[item] for item in order_items)
            total, discount, freebie = calculate_bill(order_items, menu)

            st.markdown("""
                <div style='background:#f0f4ff; padding:15px 20px; border-radius:10px; margin-top:15px; font-size:16px; box-shadow:0 2px 8px rgba(0,0,0,0.05)'>
                    <b>🧾 Order Summary:</b><br>
                    <ul style='padding-left: 20px'>
            """ + "".join([f"<li>{item} — ₹{menu[item]}</li>" for item in order_items]) + f"""
                    </ul>
                    <b>Subtotal:</b> ₹{bill}<br>
                    <b>Discount:</b> {discount}%<br>
                    <b>Final Total:</b> ₹{total:.2f}
                </div>
            """, unsafe_allow_html=True)

            if freebie:
                st.success(f"🎁 Bonus Item Included: **{freebie}**")

            st.markdown("### 🏨 Delivery Details")
            col1, col2 = st.columns(2)
            with col1:
                hostel = st.text_input("🏠 Hostel No")
            with col2:
                room = st.text_input("🚪 Room No")

            delivery_agent = get_agent(hostel)
            if delivery_agent:
                st.markdown(f"""
                    <div style='background:#e3ffe3; padding:12px; border-radius:10px; font-size:16px'>
                        🚚 <b>Assigned Delivery Agent:</b> {delivery_agent}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No agent found for this hostel.")

            st.markdown("### 💳 Payment Method")
            payment = st.radio("", ["Cash on Delivery", "Pay Online"], horizontal=True)

            if st.button("✅ Confirm Order"):
                if not hostel or not room:
                    st.error("❗ Please enter both hostel and room number.")
                else:
                    record_order(current_user, outlet, order_items, total, discount, freebie)
                    st.balloons()
                    st.success("🎉 Your order has been placed successfully!")

                    typewriter_modern(f"Thank you {current_user} for ordering from BUzaato Services India 💜", delay=0.07)

                    if payment == "Pay Online":
                        st.image(generate_qr(total), caption="📲 Scan this to Pay", width=250)
                        st.info("Please complete the payment to start food preparation.")
                    else:
                        st.info("Please pay cash to the delivery agent upon arrival. Enjoy your meal! 🍽️")
        else:
            st.warning("⚠️ Please select at least one item to proceed with your order.")


    elif menu_option == "📦 Pending Deliveries":
        st.markdown("<h2 style='color:#2c3e50;'>📦 Pending Deliveries</h2>", unsafe_allow_html=True)
        pending = get_pending_orders(current_user)
        if not pending:
            st.success("✅ All your orders have been delivered.")
        else:
            for order in pending:
                with st.expander(f"🧾 {order['timestamp']} - {order['outlet']} - ₹{order['total']}"):
                    st.write("**Items:**", order["items"])
                    st.write("**Delivery Agent:**", order.get("agent", "Not Assigned"))


                    st.warning("⏳ Status: Out for Delivery")

    elif menu_option == "📍 Track My Order":
        st.markdown("<h2 style='color:#2c3e50;'>📍 Track Your Order in Real-Time</h2>", unsafe_allow_html=True)

        tracking_info = track_order(current_user)

        if tracking_info:
            status = tracking_info["status"]
            agent = tracking_info["agent"]
            eta = tracking_info["eta"]

            # Progress bar for status
            status_stages = ["Order Confirmed", "Preparing Food", "Out for Delivery", "Delivered"]
            current_stage = status_stages.index(status) if status in status_stages else 0

            # Display visual status timeline
            st.markdown("### 🚦 Order Progress")
            for i, stage in enumerate(status_stages):
                if i < current_stage:
                    st.success(f"✅ {stage}")
                elif i == current_stage:
                    st.info(f"🕐 {stage} (In Progress...)")
                else:
                    st.warning(f"🔜 {stage}")

            # Delivery agent details
            st.markdown("---")
            st.markdown("### 👤 Delivery Agent")
            st.markdown(f"""
            - **Name:** {agent.split()[0]}
            - **Contact:** 📞 {agent.split()[-1].replace('x', '•')}
            """)

            st.markdown("### ⏱ Estimated Arrival Time")
            st.markdown(f"🕓 *Expected in:* **{eta} minutes**")

            st.success("🚚 Hang tight! Your food is on the way. 🍽️")

        else:
            st.warning("⚠️ No active order found to track.")
            st.markdown("👉 Try placing a new order from the *Place Order* section.")

    elif menu_option == "📞 Contact Support":
        st.markdown("<h2 style='color:#2c3e50;'>📞 Contact Support</h2>", unsafe_allow_html=True)
        support = get_support_info()
        st.markdown(f"""
            <div style='background:#ede7f6;padding:15px;border-radius:10px;'>
                ☎️ <b>Phone:</b> {support['phone']}<br>
                📧 <b>Email:</b> {support['email']}<br>
                🕑 <b>Hours:</b> {support['hours']}
            </div>
        """, unsafe_allow_html=True)
        st.info("You can also chat with our AI assistant for quick help.")

    elif menu_option == "📜 My Orders":
        st.markdown("<h2 style='color:#2c3e50;'>📜 Order History</h2>", unsafe_allow_html=True)
        history = get_orders(current_user)
        if not history:
            st.info("📭 You haven’t placed any orders yet.")
        else:
            for order in history:
                with st.expander(f"🧾 {order['timestamp']} - {order['outlet']} - ₹{order['total']}"):
                    st.markdown("**Items Ordered:**")
                    for item in order["items"].split(', '):
                        st.write(f"• {item}")
                    st.markdown(f"**Discount:** {order['discount']}%")
                    if order['freebie']:
                        st.markdown(f"**Freebie:** {order['freebie']}")

    elif menu_option == "💸 Offers":
        st.markdown("<h2 style='color:#2c3e50;'>💸 Current Offers</h2>", unsafe_allow_html=True)
        for min_amt, discount, freebie in discounts:
            offer = f"👉 <b>{discount}% OFF</b> on orders above ₹{min_amt}"
            if freebie:
                offer += f" + Freebie: <b>{freebie}</b>"
            st.markdown(f"""
                <div style='background:#fff3e0;padding:12px;border-radius:10px;margin-bottom:10px;'>
                    {offer}
                </div>
            """, unsafe_allow_html=True)

    elif menu_option == "Chat with BUZaato AI":
        buzaato_ai_chat()



# ---------------------- AUTH SECTION ----------------------
FAKE_USERNAME = "admin"
FAKE_PASSWORD = "pass123"

def login_section():
    st.markdown("""
    <style>
    body {
        background-color: #f2f6fc;
    }

    .card {
        background: #ffffff;
        padding: 2.5rem 2rem;
        margin-top: 3rem;
        border-radius: 1rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
        max-width: 420px;
        margin-left: auto;
        margin-right: auto;
    }

    .card h1 {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #6c63ff, #ff6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .card p {
        text-align: center;
        font-size: 16px;
        color: #666;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }

    .modern-button {
        display: inline-block;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        font-size: 15px;
        color: #fff;
        background: linear-gradient(45deg, #6c63ff, #ff6584);
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }

    .modern-button:hover {
        filter: brightness(1.05);
        box-shadow: 0 4px 14px rgba(108, 99, 255, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

    # Branding banner
    st.markdown(f"""
    <div style='text-align:center; margin-top: -30px; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 36px;
            font-weight: 800;
            background: linear-gradient(45deg, #6c63ff, #ff6584);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;'>
            BUzaato Services
        </h1>
        <p style='color:gray; font-size:16px; margin-top: -8px;'>Campus Food Reimagined 🍽️</p>
    </div>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h1>🔐 BUzaato Login</h1>", unsafe_allow_html=True)
        st.markdown("<p>Your one-stop campus food assistant 🍔</p>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", key="login_button"):
            if username == FAKE_USERNAME and password == FAKE_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try again.")

        st.markdown("</div>", unsafe_allow_html=True)

# ✅ Init session keys
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ✅ Main Logic
if st.session_state.logged_in:
    main_app()
else:
    login_section()
# ---------------------- LAUNCH ----------------------
if current_user:
    main_app()    
else:
    login_section()
