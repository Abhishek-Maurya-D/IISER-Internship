# Import necessary modules from Flask
from flask import Flask, request, jsonify

# Import the DPS protocol runner function from a custom module
from DPS_netsquid import run_dps_protocol

# Import CORS to allow cross-origin requests
from flask_cors import CORS

# Initialize the Flask web application
app = Flask(__name__)

# Enable CORS to allow the frontend (possibly hosted on another domain/port) to communicate with this backend
CORS(app)  # This allows your frontend at a different origin to call the backend

# Define a route for the endpoint '/run_protocol' that accepts POST requests
@app.route("/run_protocol", methods=["POST"])
def run_protocol():
    # Extract the JSON data sent in the POST request
    data = request.json

    # Get the value of the "protocol" key from the JSON payload
    protocol = data.get("protocol")

    # Check if the protocol requested is "dps"
    if protocol == "dps":
        # Run the DPS (Differential Phase Shift) QKD protocol using the imported function
        qber = run_dps_protocol()

        # Return the calculated QBER (Quantum Bit Error Rate) as a JSON response
        return jsonify({"qber": qber})
    else:
        # If the protocol is not supported, return an error message with status code 400
        return jsonify({"error": "Protocol not implemented"}), 400

# If this script is run directly (and not imported), start the Flask development server
if __name__ == "__main__":
    app.run(debug=True)  # Runs the app with debug mode enabled for easier development