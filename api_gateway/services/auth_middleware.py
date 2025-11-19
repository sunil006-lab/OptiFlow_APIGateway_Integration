import logging
import os
import jwt
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables securely
load_dotenv()
VALID_API_KEYS = set(os.getenv("VALID_API_KEYS", "").split(","))
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"

# Define API Key & JWT Security headers
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
security = HTTPBearer()

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def verify_api_key(api_key: str = Security(api_key_header)):
    """API Key authentication function."""
    if not api_key or api_key not in VALID_API_KEYS:
        logging.warning("Unauthorized API Key access attempt detected")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """JWT authentication function."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logging.info(f"JWT authentication successful for user: {payload.get('sub')}")
        return payload
    except jwt.ExpiredSignatureError:
        logging.warning("JWT Token has expired")
        raise HTTPException(status_code=401, detail="JWT Token has expired")
    except jwt.InvalidTokenError:
        logging.warning("Invalid JWT Token provided")
        raise HTTPException(status_code=401, detail="Invalid JWT Token")

async def auth_middleware(request: Request, call_next):
    """Middleware to authenticate each request before proceeding."""
    api_key = request.headers.get("X-API-KEY")
    auth_header = request.headers.get("Authorization")
    
    if api_key in VALID_API_KEYS:
        logging.info(f"API Key authentication successful for {request.client.host}")
    elif auth_header:
        verify_jwt_token(HTTPAuthorizationCredentials(auth_header))
    else:
        logging.warning(f"Unauthorized request from {request.client.host}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    response = await call_next(request)
    return response