from datetime import datetime
import streamlit as st
import qrcode
from io import BytesIO
import base64
import uuid
import time
from buzaato_ai import buzaato_ai_chat

global current_user


# Set up the page configuration
st.set_page_config(page_title="BUzaato Login", layout="centered")

# Function to get base64 image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

img_base64 = get_base64_image("COMPANY.jpg")

# Typewriter effect function
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

# Custom CSS for the app
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

    .stTextInput>div>div>input {
        background-color: #f9fbfd;
        border: 1px solid #d9e2ec;
        border-radius: 8px;
        padding: 0.5rem;
    }

    .stTextInput label {
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Temporary storage for users and orders
users = {}
order_history = []

# Menu data
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

# Function to calculate the bill
def calculate_bill(order_items, menu):
    bill = sum(menu[item] for item in order_items)
    for min_amount, discount, freebie in discounts:
        if bill >= min_amount:
            final = bill - (bill * discount / 100)
            return final, discount, freebie
    return bill, 0, ""

# Function to generate QR code
def generate_qr(total):
    upi_link = f"upi://pay?pa=vanshmalhotra1301@oksbi&pn=BUzaato%20Services&am={total}&cu=INR"
    qr = qrcode.make(upi_link)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    return buf

# Function to get the delivery agent
def get_agent(hostel):
    return agents.get(hostel.lower(), "❌ No delivery agent for this hostel.")

# Function to record an order
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
        "status": "Out for Delivery",  # default status
        "agent": agent,
        "eta": "20–30 mins",
        "timestamp": datetime.now().isoformat(sep=' ', timespec='seconds')
    }

    order_history.append(order)

# Function to get pending orders
def get_pending_orders(user):
    pending = [order for order in order_history if order['user'] == user and order['status'] != "Delivered"]
    return pending

# Function to track an order
def track_order(user):
    orders = get_pending_orders(user)
    if orders:
        return orders[-1]  # Return the most recent order
    return None

# Function to get support information
def get_support_info():
    return {
        "phone": "+91-8708546799",
        "email": "support@buzaato.in",
        "hours": "9:00 AM – 9:00 PM"
    }

# Login section

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}

if "hostel" not in st.session_state:
    st.session_state.hostel = ""

def login_section():
    st.markdown(f"""
        <div style='text-align:center;'>
            <img src='data:image/png;base64,{img_base64}' width='180'/>
            <h1 style='font-weight:800;
                background: linear-gradient(45deg, #6c63ff, #ff6584);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;'>BUzaato Services</h1>
            <p style='color:gray;'>Campus Food Reimagined 🍽️</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔓 Login", "🆕 Sign Up"])

    with tab1:
        username = st.text_input("👤 Username", key="login_user")
        password = st.text_input("🔒 Password", type="password", key="login_pass")
        login_clicked = st.button("🚪 Login")

        if login_clicked:
            if username == "admin" and password == "admin123":
                st.success("✅ Admin login successful!")
                st.stop()
            elif username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.current_user = username
                st.success(f"✅ Welcome back, {username}!")
                typewriter_modern("Loading BUzaato dashboard...", delay=0.05)
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

    with tab2:
        new_user = st.text_input("👤 Create Username", key="new_user")
        new_pass = st.text_input("🔒 Create Password", type="password", key="new_pass")
        signup_clicked = st.button("📝 Create Account")

        if signup_clicked:
            if new_user in st.session_state.users:
                st.warning("⚠️ That username is already taken.")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("🎉 Account created successfully!")
                typewriter_modern(f"Welcome {new_user} to BUzaato! 💜", delay=0.06)
                main_app()


# Main application
def main_app():
    st.sidebar.title("🍱 BUzaato Menu Hub")
    st.markdown("""
    <style>
    body {
        background-color: #f3f4f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
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
            👋 Welcome <span style='color:#2c3e50;'>{st.session_state.current_user}
</span> – <i>BUzaato Services India</i>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar branding
    st.sidebar.markdown("### 🍽️ <span style='color:#2c3e50;'>BUzaato Services</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<span style='color:#455a64;'>👤 Logged in as:</span> <code>{st.session_state.current_user}</code>", unsafe_allow_html=True)
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
                    record_order({st.session_state.current_user}, outlet, order_items, total, discount, freebie)
                    st.balloons()
                    st.success("🎉 Your order has been placed successfully!")

                    typewriter_modern(f"Thank you {{st.session_state.current_user}} for ordering from BUzaato Services India 💜", delay=0.07)

                    if payment == "Pay Online":
                        st.image(generate_qr(total), caption="📲 Scan this to Pay", width=250)
                        st.info("Please complete the payment to start food preparation.")
                    else:
                        st.info("Please pay cash to the delivery agent upon arrival. Enjoy your meal! 🍽️")
        else:
            st.warning("⚠️ Please select at least one item to proceed with your order.")

    elif menu_option == "📦 Pending Deliveries":
        st.markdown("<h2 style='color:#2c3e50;'>📦 Pending Deliveries</h2>", unsafe_allow_html=True)
        pending = get_pending_orders({st.session_state.current_user}
)
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

        tracking_info = track_order({st.session_state.current_user}
)

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
        if not order_history:
            st.info("📭 You haven’t placed any orders yet.")
        else:
            for order in order_history:
                if order['user'] == {st.session_state.current_user}:
                    with st.expander(f"🧾 {order['timestamp']} - {order['outlet']} - ₹{order['total']}"):
                        st.markdown("**Items Ordered:**")
                        for item in order["items"].split(', '):
                            st.write(f"• {item}")
                        st.markdown(f"**Discount:** {order['discount']}%")
                        if order['freebie']:
                            st.markdown(f"**Freebie:** {order['freebie']}")
    elif menu_option == "Chat with BUZaato AI":
        buzaato_ai_chat()
# Launch the application
if st.session_state.current_user:
    main_app()
else:
    login_section()
