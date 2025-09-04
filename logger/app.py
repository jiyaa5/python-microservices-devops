from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Ensure log directory exists
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "requests.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/log", methods=["POST"])
def log_request():
    data = request.get_json()
    logging.info(f"Request logged: {data}")
    return jsonify({"status": "logged"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
