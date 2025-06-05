from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def handle_message():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = f"You said: {user_message}"
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
