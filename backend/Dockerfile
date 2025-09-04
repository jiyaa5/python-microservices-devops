FROM python:3.11-slim
WORKDIR /app
COPY requirements_.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
