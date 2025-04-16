# utils/planner.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan(topic: str) -> str:
    prompt = f"""
你是一位 DevOps 教練，請幫我為「{topic}」規劃一個四步驟的學習計畫，每步驟要有主題與簡短說明，不需要使用 markdown。
請用中文回覆。
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 發生錯誤：{e}"
