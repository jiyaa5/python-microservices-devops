from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Disable Flask's default logging
logging.getLogger('werkzeug').disabled = True

os.makedirs("/app/logs", exist_ok=True)

# Configure our logging
logging.basicConfig(
    filename="/app/logs/requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

@app.route("/log", methods=["POST"])
def log_request():
    data = request.get_json()
    logging.info(f"Request logged: {data}")
    return jsonify({"status": "logged"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
