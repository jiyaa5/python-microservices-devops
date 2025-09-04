from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route("/api/data", methods=["GET"])
def get_data():
    response = {"message": "Hello from Backend API!"}

    # Send log info to logger
    try:
        logger_url = os.getenv("LOGGER_URL", "http://logger:5002/log")
        requests.post(logger_url, json={"endpoint": "/api/data", "method": "GET"})
    except Exception as e:
        print(f"Logger not available: {e}")

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # port=5000 (frontend expects this!)
