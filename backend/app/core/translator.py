from typing import Dict, Any
from .nlp import extract_entities_and_intent

def nl_to_dsl(nl_query: str) -> Dict[str, Any]:
    """Convert natural language query to Elasticsearch DSL"""
    # Extract entities and intent
    parsed = extract_entities_and_intent(nl_query)
    
    # Simple mock translation - enhance with actual logic
    dsl_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"message": nl_query}}
                ]
            }
        },
        "size": 100,
        "sort": [
            {"@timestamp": {"order": "desc"}}
        ]
    }
    
    return {
        "dsl": dsl_query,
        "intent": parsed.get("intent", "unknown"),
        "entities": parsed.get("entities", {})
    }