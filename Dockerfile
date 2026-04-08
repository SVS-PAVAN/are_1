FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pydantic openai requests

ENV ENABLE_WEB_INTERFACE=true
CMD ["python", "-m", "server.app"]