# 選用 base image
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製檔案並安裝依賴
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# 👇 最重要：Cloud Run 預設只開放 8080！
ENV PORT 8080
EXPOSE 8080

# 使用 gunicorn 或 flask 指定 host + port
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
