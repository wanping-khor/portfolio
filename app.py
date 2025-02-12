import os
import json
import logging
from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS")
if not creds_json:
    logging.error("GOOGLE_CREDENTIALS environment variable not found!")
    creds = None
    client = None
else:
    try:
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
    except Exception as e:
        logging.error(f"Error loading Google credentials: {e}")
        creds = None
        client = None

# Google Sheet ID
SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo"
sheet = None

if client:
    try:
        sheet = client.open_by_key(SHEET_ID).sheet1
    except Exception as e:
        logging.error(f"Error accessing Google Sheet: {e}")
        sheet = None

@app.route("/", methods=['GET'])
def home():
    """Home route to confirm the API is running."""
    return jsonify({"message": "Flask is running! Use /data to fetch Google Sheets data."})

@app.route('/data', methods=['GET'])
def get_data():
    """Fetch all records from Google Sheets."""
    if not sheet:
        return jsonify({"error": "Google Sheets not accessible"}), 500
    
    try:
        data = sheet.get_all_records()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching data from Google Sheets: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500

@app.route('/debug_credentials', methods=['GET'])
def debug_credentials():
    """Debug route to check if credentials are loaded properly."""
    return jsonify({"GOOGLE_CREDENTIALS": creds_json if creds_json else "No credentials found"})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Get the port from environment variables
    app.run(host="0.0.0.0", port=port, debug=True)
