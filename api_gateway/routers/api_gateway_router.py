from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import redis
import logging

# Configure Redis for dynamic traffic tracking
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Configure logging for monitoring and debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()


class RouteTraffic(BaseModel):
    path: str
    method: str
    hits: int
    status: str


class RouteTrafficResponse(BaseModel):
    routes: List[RouteTraffic]


def fetch_traffic_stats():
    """Fetch real-time route traffic stats from Redis."""
    routes = []
    for key in redis_client.keys("route_stats:*"):
        data = redis_client.hgetall(key)
        routes.append(
            {
                "path": data["path"],
                "method": data["method"],
                "hits": int(data.get("hits", 0)),
                "status": data["status"],
            }
        )
    return routes


def increment_route_hits(path: str, method: str):
    """Increment route hit count in Redis dynamically."""
    key = f"route_stats:{path}:{method}"
    if not redis_client.exists(key):
        redis_client.hset(key, mapping={"path": path, "method": method, "hits": 1, "status": "OK"})
    else:
        redis_client.hincrby(key, "hits", 1)


@router.get("/api/traffic/routes", response_model=RouteTrafficResponse)
async def get_route_traffic():
    """Retrieve real-time API Gateway traffic stats."""
    logging.info("Traffic route stats requested")
    stats = fetch_traffic_stats()
    return {"routes": stats}


@router.post("/api/traffic/update")
async def update_route_hits(path: str, method: str):
    """Increment hit count for a specific route."""
    if not path or not method:
        raise HTTPException(status_code=400, detail="Invalid path or method")
    
    increment_route_hits(path, method)
    logging.info(f"Route hit updated: {path} [{method}]")
    return {"message": f"Updated hit count for {path} [{method}]"}