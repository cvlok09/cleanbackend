from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def handle_message():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Example reply
    reply = f"You said: {user_message}"
    
    return jsonify({"response": reply})
