import json
import os
from typing import Optional, Dict, Any

import redis

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
try:
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    # Test connection briefly
    r.ping()
except Exception:
    # Fallback to localhost if the provided host is not reachable
    try:
        r = redis.Redis.from_url("redis://127.0.0.1:6379/0", decode_responses=True)
        r.ping()
    except Exception:
        # Last-resort: create a client that will error at call time
        r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def store_query(query_id: str, query_data: Dict[Any, Any]) -> bool:
    """Store query data in Redis"""
    try:
        r.setex(f"query:{query_id}", 3600, json.dumps(query_data))  # 1 hour expiry
        return True
    except Exception as e:
        print(f"Error storing query: {e}")
        return False

def get_query(query_id: str) -> Optional[Dict[Any, Any]]:
    """Retrieve query data from Redis"""
    try:
        data = r.get(f"query:{query_id}")
        return json.loads(data) if data else None
    except Exception as e:
        print(f"Error retrieving query: {e}")
        return None