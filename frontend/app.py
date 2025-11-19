from flask import Flask, render_template, jsonify
import requests
import os
import logging

# Configure logging for better debugging and tracking
#logging.basicConfig(level=logging.INFO)
# Configure logging
logging.basicConfig(
    filename="api_gateway.log",  # Store logs in a file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



# Load API Gateway URL dynamically from environment variables
FASTAPI_GATEWAY_URL = os.getenv("FASTAPI_GATEWAY_URL", "http://localhost:5000")

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def dashboard():
    print("Inside app.py dashboard fun\n")
    return render_template('index.html')

@app.route('/data')
def get_data():
    print("Inside app.py get_data fun data route\n")
    try:
        response = requests.get(f"{FASTAPI_GATEWAY_URL}/data", timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"API Gateway request failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500

if __name__ == '__main__':
    # Production considerations:
    # - Remove debug=True for deployment
    # - Use Gunicorn or uWSGI instead of Flask's built-in server
    # - Enable HTTPS for API calls
    app.run(host="0.0.0.0", port=5000)