from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from app.core.translator import nl_to_dsl
from app.core.elastic_client import run_query
from app.core.redis_store import store_query
from app.core.hf_client import generate_rag_answer, format_search_hits
import uuid
from datetime import datetime

router = APIRouter()

class NLQuery(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    query_id: str
    dsl: dict
    explanation: str
    answer: str
    context: List[str] = Field(default_factory=list)
    result: dict
    timestamp: str

@router.post("/", response_model=QueryResponse)
def converse(query: NLQuery):
    try:
        # Generate unique query ID
        query_id = str(uuid.uuid4())
        
        # Translate natural language to DSL
        translation_result = nl_to_dsl(query.query)
        
        # Execute query (currently mock)
        search_result = run_query("security-logs", translation_result["dsl"])
        
        # Convert ObjectApiResponse to dict if needed
        if hasattr(search_result, 'body'):
            search_result = search_result.body
        elif not isinstance(search_result, dict):
            search_result = dict(search_result)

        context = format_search_hits(search_result)
        answer = generate_rag_answer(
            query.query,
            search_result,
            intent=translation_result.get("intent"),
        )
        
        # Store query for later reference
        query_data = {
            "user_id": query.user_id,
            "original_query": query.query,
            "dsl": translation_result["dsl"],
            "result": search_result,
            "answer": answer,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        store_query(query_id, query_data)
        
        return QueryResponse(
            query_id=query_id,
            dsl=translation_result["dsl"],
            explanation=f"Translated '{query.query}' to Elasticsearch DSL query and generated a Hugging Face grounded answer",
            answer=answer,
            context=context,
            result=search_result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


