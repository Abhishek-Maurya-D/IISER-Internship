from flask import Flask, request, jsonify
from DPS_netsquid import run_dps_protocol
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This allows your frontend at a different origin to call the backend
@app.route("/run_protocol", methods=["POST"])
def run_protocol():
    data = request.json
    protocol = data.get("protocol")

    if protocol == "dps":
        qber = run_dps_protocol()
        return jsonify({"qber": qber})
    else:
        return jsonify({"error": "Protocol not implemented"}), 400

if __name__ == "__main__":
    app.run(debug=True)
