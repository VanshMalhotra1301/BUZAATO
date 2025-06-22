from supabase import create_client, Client
from datetime import datetime

# 🔑 Replace with your actual credentials
SUPABASE_URL = "https://wxgutoplztcprlkbhbtb.supabase.co"  # <-- Replace this
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4Z3V0b3BsenRjcHJsa2JoYnRiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1OTYxMTgsImV4cCI6MjA2NjE3MjExOH0.PdsAaF407jUQBJpSQFvMMlVtmmWEFQt2lCuJxbZjjaA"                           # <-- Replace this

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_user(username, password):
    try:
        response = supabase.table("users").insert({
            "username": username,
            "password": password
        }).execute()
        return True
    except Exception as e:
        print("Error in create_user:", e)
        return False

def check_user(username, password):
    try:
        result = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        return len(result.data) > 0
    except Exception as e:
        print("Error in check_user:", e)
        return False

def insert_order(username, outlet, items, total, discount, freebie, timestamp=None):
    try:
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        response = supabase.table("orders").insert({
            "username": username,
            "outlet": outlet,
            "items": ", ".join(items),
            "total": float(total),
            "discount": discount,
            "freebie": freebie,
            "timestamp": timestamp
        }).execute()
        return True
    except Exception as e:
        print("Error in insert_order:", e)
        return False

def get_orders(username):
    try:
        response = supabase.table("orders").select("*").eq("username", username).order("timestamp", desc=True).execute()
        return response.data
    except Exception as e:
        print("Error in get_orders:", e)
        return []
