import os
import json
import logging
from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 允许跨域请求
from flask_cors import CORS
CORS(app)

# 🔹 1. 载入 .env 文件
load_dotenv()

# 🔹 2. 设置 Google Sheets API 认证
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

if not creds_path:
    logging.error("❌ GOOGLE_CREDENTIALS_PATH 未设置！")
    creds = None
    client = None
else:
    try:
        with open(creds_path, "r") as f:
            creds_dict = json.load(f)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        logging.info("✅ Google Sheets 认证成功！")
    except Exception as e:
        logging.error(f"❌ Google 认证失败: {e}")
        creds = None
        client = None

# 🔹 3. 设置 Google Sheet ID
SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo"
sheet = None

if client:
    try:
        sheet = client.open_by_key(SHEET_ID).sheet1
        logging.info("✅ 成功连接到 Google Sheet！")
    except Exception as e:
        logging.error(f"❌ 连接 Google Sheet 失败: {e}")
        sheet = None

# 🔹 4. 创建 API 端点
@app.route("/api/data", methods=["GET"])
def get_data():
    """从 Google Sheets 获取所有数据"""
    if not sheet:
        return jsonify({"error": "Google Sheets 无法访问"}), 500
    
    try:
        data = sheet.get_all_records()
        return jsonify(data)
    except Exception as e:
        logging.error(f"❌ 获取数据失败: {e}")
        return jsonify({"error": "无法获取数据"}), 500

# 🔹 5. 启动 Flask 服务器
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 允许 Heroku 读取 PORT 变量
    app.run(debug=True, port=port)
