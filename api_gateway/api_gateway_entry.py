from fastapi import FastAPI, Request, HTTPException, Depends
import logging
import redis
import jwt
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv  # Secure environment variable handling

# Load environment variables from a .env file
load_dotenv()

# Secure API Keys and JWT Secret
VALID_API_KEYS = set(os.getenv("VALID_API_KEYS", "").split(","))
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"

# API Gateway Configuration
API_GATEWAY_IP = os.getenv("API_GATEWAY_IP", "192.168.1.100")
API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT", 8080))
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))  # Max requests per minute per client

# Initialize FastAPI
app = FastAPI()
security = HTTPBearer()

# Redis for Rate Limiting
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Configure Structured Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def auth_middleware(request: Request, credentials: HTTPAuthorizationCredentials = None):
    """Enhanced authentication middleware supporting API keys and JWT tokens."""
    
    api_key = request.headers.get("X-API-KEY")
    if api_key and api_key in VALID_API_KEYS:
        logging.info(f"API Key authentication successful for key: {api_key}")
        return
    
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            if "sub" in payload:
                logging.info(f"JWT authentication successful for user: {payload['sub']}")
                return
        except jwt.ExpiredSignatureError:
            logging.warning("JWT Token has expired")
            raise HTTPException(status_code=401, detail="JWT Token has expired")
        except jwt.InvalidTokenError:
            logging.warning("Invalid JWT Token provided")
            raise HTTPException(status_code=401, detail="Invalid JWT Token")
    
    logging.error("Unauthorized access attempt detected")
    raise HTTPException(status_code=401, detail="Unauthorized")


def rate_limiter(request: Request):
    """Enhanced rate limiting per API key rather than IP for better control."""
    api_key = request.headers.get("X-API-KEY", "")
    client_identifier = api_key if api_key in VALID_API_KEYS else request.client.host
    key = f"rate_limit:{client_identifier}"
    
    requests = redis_client.get(key)
    
    if requests is None:
        redis_client.setex(key, 60, 1)
    else:
        if int(requests) >= RATE_LIMIT:
            logging.warning(f"Rate limit exceeded for {client_identifier}")
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
        redis_client.incr(key)


@app.get("/", dependencies=[Depends(rate_limiter)], tags=["OptiFlow APIGW"])
async def read_root():
    """API Gateway Root Endpoint"""
    logging.info("Root endpoint accessed")
    return {"message": "Welcome to OptiFlow AI-OrchestrateX Gateway!", "ip": API_GATEWAY_IP}


@app.get("/health", tags=["Healthcheck"])
async def health_check():
    """Health Check for API Gateway"""
    logging.info("Health check requested")
    return {"status": "API Gateway is running", "ip": API_GATEWAY_IP}


@app.post("/route", dependencies=[Depends(rate_limiter), Depends(auth_middleware)], tags=["Routing"])
async def route_request(payload: dict):
    """Route requests to the core engine based on orchestration logic"""
    logging.info(f"Routing request: {payload}")
    return {"status": "Request forwarded to core engine", "data": payload}


if __name__ == "__main__":
    import uvicorn
    logging.info("Starting API Gateway...")
    uvicorn.run(app, host=API_GATEWAY_IP, port=API_GATEWAY_PORT)