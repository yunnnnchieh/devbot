from openai import OpenAI
import os

# 建立 OpenAI client，建議你從 .env 載入 API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_plan(task_name: str) -> str:
    prompt = f"""
你是一位專業任務規劃助手，請幫我針對「{task_name}」這個主題，設計一個簡單三步驟的學習/實作計畫，一天可以做完的任務，每步驟一句話說明即可。
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是專業的任務分解與學習計畫助手。"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
