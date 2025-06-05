from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        reply = f"You said: {user_message}"
        return jsonify({"response": reply})
    except Exception as e:
        # ✅ Print the error to your logs
        print("Error occurred:", e)
        traceback.print_exc()
        return jsonify({"response": "Server error occurred."}), 500
