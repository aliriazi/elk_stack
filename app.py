from fastapi import FastAPI, Request
import structlog
import logging
import socket
import json

# Setup JSON logging
structlog.configure(
    processors=[structlog.processors.JSONRenderer()],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logger = structlog.get_logger()

app = FastAPI()

LOGSTASH_HOST = "localhost"
LOGSTASH_PORT = 5000

def send_log_to_logstash(log_data: dict):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        sock.send((json.dumps(log_data) + "\n").encode("utf-8"))
        sock.close()
    except Exception as e:
        print("Failed to send log:", e)

@app.get("/")
async def root(request: Request):
    log_data = {
        "service": "user-service",
        "endpoint": "/",
        "method": "GET",
        "client_ip": request.client.host,
        "status": 200,
        "message": "Hello from root!",
    }
    send_log_to_logstash(log_data)
    return {"message": "Hello World"}

@app.get("/health")
async def health(request: Request):
    log_data = {
        "service": "user-service",
        "endpoint": "/health",
        "method": "GET",
        "client_ip": request.client.host,
        "status": 200,
        "message": "Health check OK",
    }
    send_log_to_logstash(log_data)
    return {"status": "ok"}

