from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host='db',
        database='login_db',
        user='postgres',
        password='postgres'
    )

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"status": "success", "message": "Login successful!"})
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/api/init', methods=['GET'])
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)
    cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123') ON CONFLICT DO NOTHING;")
    conn.commit()
    cur.close()
    conn.close()
    return "Database initialized!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
