from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json
import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# Load OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load Google credentials
google_creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = service_account.Credentials.from_service_account_info(google_creds)
sheets_service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]

@app.route("/", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # Use OpenAI to interpret the message
        system_prompt = (
            "You are a smart assistant for a fraternity. "
            "You manage a Google Sheet that logs dues, payments, and contact info. "
            "If a user says something like 'George paid his dues in full' or 'change Joe's email to joe@email.com', "
            "you interpret the intent and respond accordingly. Keep responses helpful and conversational."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message["content"]

        # Log to Google Sheet (append for now)
        sheet = sheets_service.spreadsheets()
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Logs!A:C",
            valueInputOption="USER_ENTERED",
            body={"values": [[user_message, reply]]}
        ).execute()

        return jsonify({"response": reply})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"response": "Sorry, something went wrong on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
