
#!/usr/bin/env python
# coding: utf-8

import asyncio
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
import random
import redis.asyncio as aioredis  # For caching and predictive scaling
from kafka import KafkaProducer, KafkaConsumer  # For event-driven architecture

# Configuration Variables
API_GATEWAY_IP = "192.168.1.100"  # Replace with actual IP if needed
PORT = 8080  # Specify the port
KAFKA_BROKER = "localhost:9092"  # Kafka broker for event-driven processing
KAFKA_TOPIC = "Kafka-test"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

# Initialize FastAPI app
app = FastAPI(
    title="OptiFlow AI-OrchestrateX Gateway",
    description="An AI-powered API Gateway with predictive scaling and smart traffic routing.",
    version="3.0.0",
)

router = APIRouter()

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis for caching & AI-driven optimizations
async def get_redis():
    return await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

# Kafka Consumer
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER, auto_offset_reset='earliest', group_id='new-optiflow-group')

# Pydantic Model for Request Validation
class DataInput(BaseModel):
    key: str
    value: int




@app.post("/producer", tags=["Kafka-producer"])
async def produce_message(input_data: DataInput):
    """Produces messages to Kafka."""
    try:
        producer.send(KAFKA_TOPIC, f"{input_data.key}: {input_data.value}".encode())
        logging.info(f"Produced message: {input_data.key}: {input_data.value}")
        return {"message": "Message sent to Kafka", "data": input_data.dict()}
    except Exception as e:
        logging.error(f"Error in producer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in producer: {str(e)}")

@app.get("/consumer", tags=["Kafka-consumer"])
async def consume_messages():
    """Consumes messages from Kafka."""
    try:
        messages = []
        logging.info("Starting Kafka Consumer...")

        consumer = KafkaConsumer(
            "your_topic",
            bootstrap_servers="localhost:9092",
            group_id="new-optiflow-group",
            auto_offset_reset="earliest",
        )

        for msg in consumer:
            messages.append(msg.value.decode())
            if len(messages) >= 5:
                break

        logging.info(f"Consumed messages: {messages}")
        return {"messages": messages}
    
    except Exception as e:
        logging.error(f"Error in consumer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in consumer: {str(e)}")


@app.get("/health")
async def health_check():
    """Performs AI-driven health diagnostics."""
    try:
        load_status = random.choice(["low", "medium", "high"])  # Simulated AI workload analysis
        logging.info(f"Health check: Load status {load_status}")
        return {"status": "ok", "uptime": f"{time.time()} seconds", "load_status": load_status}
    except Exception as e:
        logging.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in health check: {str(e)}")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        config = uvicorn.Config(
            app,
            host=API_GATEWAY_IP,
            port=PORT,
            log_level="info",
            reload=True
        )
        server = uvicorn.Server(config)
        logging.info("Starting Uvicorn server...")
        loop.run_until_complete(server.serve())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        logging.warning("Runtime error occurred. Applying nest_asyncio.")
        uvicorn.run(app, host=API_GATEWAY_IP, port=PORT, log_level="info", reload=True)
