from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Explicitly allow requests from your frontend on Vercel
CORS(app, resources={r"/*": {"origins": "https://lambdabotclean.vercel.app"}})

@app.route("/", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        reply = f"You said: {user_message}"
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": "Server error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
