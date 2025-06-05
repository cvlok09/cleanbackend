from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for frontend)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Backend is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Dummy response – replace with real logic
        response = f"You said: {message}"
        return jsonify({"reply": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
