import os
from flask import Flask, request, abort, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from utils.planner import generate_plan
from utils.recorder import record_progress, get_records
from utils.visualizer import generate_progress_chart
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def index():
    return "✅ DevTrackBot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()

    if msg.startswith("/plan"):
        task = msg.replace("/plan", "").strip()
        plan = generate_plan(task)
        reply = f"以下是針對「{task}」的任務規劃：\n{plan}"
    elif msg.startswith("/progress"):
        content = msg.replace("/progress", "").strip()
        record_progress(content)
        reply = f"✅ 已記錄你的進度：「{content}」"
    elif msg == "/visual":
        chart_path = generate_progress_chart()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=os.getenv("PUBLIC_URL") + "/chart",
                preview_image_url=os.getenv("PUBLIC_URL") + "/chart"
            )
        )
        return
    elif msg == "/deploy":
        reply = "🚀 模擬觸發 GitHub Webhook，自動部署啟動！（示意）"
    else:
        reply = f"你說了：{msg}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

@app.route("/chart")
def serve_chart():
    return send_file("progress_chart.png", mimetype="image/png")
