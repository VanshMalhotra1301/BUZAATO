import mysql.connector
from mysql.connector import Error

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # your MySQL username
        password="ww22iixxzz",    # your MySQL password
        database="buzatto"
    )

def create_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def insert_order(username, outlet, items, total, discount, freebie, timestamp):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (username, outlet, items, total, discount, freebie, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, outlet, ', '.join(items), total, discount, freebie, timestamp)
    )
    conn.commit()
    conn.close()

def get_orders(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE username=%s ORDER BY timestamp DESC", (username,))
    result = cursor.fetchall()
    conn.close()
    return result
