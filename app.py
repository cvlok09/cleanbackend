from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import os
import json
import openai

from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# Load environment variables
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDENTIALS")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

# Parse service account credentials and create Sheets client
try:
    creds_dict = json.loads(GOOGLE_CREDS)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheets_service = build("sheets", "v4", credentials=creds)
    sheet = sheets_service.spreadsheets()
except Exception as e:
    print("❌ Error initializing Google Sheets client:")
    print(e)
    traceback.print_exc()

@app.route("/", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please send a message."})

        # AI response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": user_message }]
        )
        reply = response.choices[0].message.content.strip()

        # Optionally log the interaction to Google Sheets (e.g., log messages)
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Log!A1",
            valueInputOption="RAW",
            body={"values": [[user_message, reply]]}
        ).execute()

        return jsonify({ "response": reply })

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        print(e)
        traceback.print_exc()
        return jsonify({ "response": "Server error occurred." }), 500

if __name__ == "__main__":
    app.run(debug=True)
