import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import os
import logging
import signal
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from api_gateway.routers import api_gateway_router
import uvicorn

# Load environment variables securely
load_dotenv()
API_GATEWAY_IP = os.getenv("API_GATEWAY_IP", "192.168.1.100")
API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT", "8080"))

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Initializing OptiFlow API Gateway...")

app = FastAPI(title="OptiFlow API Gateway")

# Include router
app.include_router(api_gateway_router.router)

def shutdown_server(signal_received, frame):
    """Graceful shutdown of API Gateway"""
    logging.info("Shutting down OptiFlow API Gateway...")
    sys.exit(0)

# Handle shutdown signals for clean exit
signal.signal(signal.SIGINT, shutdown_server)
signal.signal(signal.SIGTERM, shutdown_server)

if __name__ == "__main__":
    logging.info(f"Starting OptiFlow API Gateway at {API_GATEWAY_IP}:{API_GATEWAY_PORT}")
    uvicorn.run(app, host=API_GATEWAY_IP, port=API_GATEWAY_PORT)