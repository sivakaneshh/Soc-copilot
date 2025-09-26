import redis
import json
from typing import Optional, Dict, Any

# Redis connection
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

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