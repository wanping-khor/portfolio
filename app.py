from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route('/data', methods=['GET'])
def get_data():
    data = sheet.get_all_records()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
