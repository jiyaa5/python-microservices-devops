import os
import psycopg2
from flask import Flask, jsonify, request
import requests
import datetime

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres", 
        database=os.environ.get("POSTGRES_DB", "mydb"),
        user=os.environ.get("POSTGRES_USER", "user"),
        password=os.environ.get("POSTGRES_PASSWORD", "password")
    )
    return conn

# API endpoint
@app.route("/api/data", methods=["GET"])
def get_data():
    # Backend response
    response = {"message": "Hello from Backend API!"}

    # Send log to logger service
    try:
        logger_url = os.getenv("LOGGER_URL", "http://logger:5002/log")
        requests.post(logger_url, json={
            "endpoint": "/api/data",
            "method": "GET",
            "timestamp": str(datetime.datetime.now())
        })
    except Exception as e:
        print(f"Logger not available: {e}")

    # Store API call in PostgreSQL
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE
            );
        """)
        
        # Insert a test user
        cur.execute("""
            INSERT INTO users (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """, ("test_user_from_backend",))
        
        # Fetch all users
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        
        response["users"] = [{"id": row[0], "name": row[1]} for row in users]
    
    except Exception as e:
        response["db_error"] = str(e)

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
