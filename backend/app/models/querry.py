from pydantic import BaseModel
from typing import Optional, Dict, Any

class Query(BaseModel):
    user_id: str
    query: str
    timestamp: Optional[str] = None
    processed_query: Optional[str] = None
    dsl_result: Optional[Dict[Any, Any]] = None