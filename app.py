import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 初始化 LINE 與 OpenAI
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 👉 在這裡貼上你的履歷文字
resume_text = """
我在 10 多個 Web 專案中累積了前後端整合、系統架構設計與效能優化的經驗。對資安的興趣也讓我深入理解攻防思維並將其應用於開發安全應用上。具備良好抗壓能力與溝通協作技巧，適應快速變動的開發節奏，喜歡參與 Hackathon 和團隊合作。

目前希望能加入 LINE 擔任 Software Development Intern，參與前後端開發、CI/CD、測試與產品設計，並優化系統架構與前端體驗。

【技能】
- 前端：Vue.js, Nuxt.js, React, JavaScript, TypeScript
- 後端：Java (Spring Boot), Python (Flask), Node.js/Express.js
- 資料庫：MySQL, PostgreSQL, MongoDB, Redis, Firebase, SQLite
- DevOps：Docker, Kubernetes, GitLab CI/CD, GitHub Actions, Helm, Nginx
- 工具：Figma, Jira, Git, GCP
- 專案管理：Agile 敏捷開發

【專案經驗】
NCU 新生資訊系統（團隊領導）
- 將 Figma 設計轉為 Vue.js 網頁，提升使用者體驗與可及性
- 設計 MySQL+Redis 資料儲存機制，實現快速讀寫與一致性
- 實作 CI/CD pipeline 加速部署流程，自動化測試與版本更新
- 使用 Helm 配置 K8s 應用，設置 Secret、定時備份與負載均衡

發票管家：AI 財務應用
- 使用 Nuxt.js + Tailwind CSS 建立前端視覺化頁面
- 後端使用 FastAPI + SQL 整合 GPT 分析花費分類並生成圖表
- 以 Docker 建置微服務架構，部署至 GCP，並加上監控機制

【實習與職場經歷】
國立中央大學電子計算中心（網路管理員）
- 自動化系統部署流程（使用 Bash/Python/PowerShell）
- 設定與管理 DHCP、VLAN、Firewall 與 NAT 規則
- 管理 Linux/Windows Server，優化效能與日誌分析

教育部資安演練（紅隊成員）
- 使用 Kali/Windows 環境進行滲透測試與漏洞分析
- 模擬 SQLi, XSS, SSRF, Broken Access Control 等攻擊
- 產出修補建議報告，提升防禦架構與通報能力

【競賽與成就】
- InnoServe Awards 入圍
- Taipei Smart City 青年政策提案佳作
- Girls in CyberSecurity、SITCON x Hackathon 參與者

【語言能力】
- 中文（母語）
- 英文（流利，TOEIC 905）
- 韓文（學習中，預計 2025 TOPIK II 應考）

【證照】
- Google IT Support、Google Cybersecurity、Google Cloud Security
- AWS Cloud Consultant（含雲端與資料庫設計技能）

我擅長用技術創造解決方案，也樂於學習新領域，未來希望能在 LINE 的開發平台上實現更多跨系統的創新整合。
"""


@app.route("/")
def index():
    return "✅ LINE Bot 啟動成功！"

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
    user_question = event.message.text.strip()

    messages = [
        {
            "role": "system",
            "content": "你是一位人資助理，請根據以下履歷用『第一人稱』的語氣回答使用者的問題，像是我本人在回答。"
        },
        {"role": "user", "content": f"履歷內容如下：\n{resume_text}"},
        {"role": "user", "content": f"問題：{user_question}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"❌ 錯誤：{e}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=answer)
    )
