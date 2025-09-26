from typing import Dict, Any
import re
from datetime import datetime, timedelta

def nl_to_dsl(nl_query: str) -> Dict[str, Any]:
    """Convert natural language query to Elasticsearch DSL"""
    query_lower = nl_query.lower()
    
    # Initialize base query structure
    must_clauses = []
    filter_clauses = []
    
    # Extract time range
    time_filter = extract_time_range(query_lower)
    if time_filter:
        filter_clauses.append(time_filter)
    
    # Extract IP addresses
    ip_matches = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', nl_query)
    for ip in ip_matches:
        must_clauses.append({
            "bool": {
                "should": [
                    {"term": {"source_ip": ip}},
                    {"term": {"dest_ip": ip}}
                ]
            }
        })
    
    # Extract usernames
    user_match = re.search(r'(?:user|username|account)\s+(\w+)', query_lower)
    if user_match:
        username = user_match.group(1)
        must_clauses.append({"term": {"user": username}})
    
    # Detect query patterns
    if any(word in query_lower for word in ['failed', 'failure', 'unsuccessful']):
        if 'login' in query_lower or 'authentication' in query_lower:
            must_clauses.append({"term": {"log_type": "authentication"}})
            must_clauses.append({"term": {"status": "failed"}})
        
    elif any(word in query_lower for word in ['successful', 'success']):
        if 'login' in query_lower or 'authentication' in query_lower:
            must_clauses.append({"term": {"log_type": "authentication"}})
            must_clauses.append({"term": {"status": "success"}})
    
    elif 'network' in query_lower or 'connection' in query_lower:
        must_clauses.append({"term": {"log_type": "network"}})
    
    elif 'system' in query_lower or 'process' in query_lower:
        must_clauses.append({"term": {"log_type": "system"}})
    
    elif any(word in query_lower for word in ['error', 'warning', 'critical']):
        severity_terms = []
        if 'error' in query_lower:
            severity_terms.append("error")
        if 'warning' in query_lower:
            severity_terms.append("warning")
        if 'critical' in query_lower:
            severity_terms.append("critical")
        
        if severity_terms:
            must_clauses.append({"terms": {"severity": severity_terms}})
    
    elif any(word in query_lower for word in ['suspicious', 'anomaly', 'threat']):
        must_clauses.append({
            "bool": {
                "should": [
                    {"match": {"message": "suspicious"}},
                    {"match": {"message": "anomaly"}},
                    {"match": {"message": "threat"}},
                    {"term": {"severity": "warning"}},
                    {"term": {"severity": "error"}}
                ]
            }
        })
    
    # If no specific patterns found, do a general text search
    if not must_clauses:
        must_clauses.append({"multi_match": {
            "query": nl_query,
            "fields": ["message", "user", "host", "event_type"],
            "type": "best_fields"
        }})
    
    # Build final query
    dsl_query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "filter": filter_clauses
            }
        },
        "size": 100,
        "sort": [
            {"@timestamp": {"order": "desc"}}
        ]
    }
    
    return {
        "dsl": dsl_query,
        "intent": detect_intent(query_lower),
        "entities": extract_entities(nl_query)
    }

def extract_time_range(query: str) -> Dict[str, Any]:
    """Extract time range from natural language query"""
    now = datetime.now()
    
    if 'last hour' in query or 'past hour' in query:
        return {"range": {"@timestamp": {"gte": (now - timedelta(hours=1)).isoformat()}}}
    elif 'last 24 hours' in query or 'past day' in query or 'today' in query:
        return {"range": {"@timestamp": {"gte": (now - timedelta(days=1)).isoformat()}}}
    elif 'last week' in query or 'past week' in query:
        return {"range": {"@timestamp": {"gte": (now - timedelta(weeks=1)).isoformat()}}}
    elif 'last month' in query or 'past month' in query:
        return {"range": {"@timestamp": {"gte": (now - timedelta(days=30)).isoformat()}}}
    
    return None

def detect_intent(query: str) -> str:
    """Detect the intent of the query"""
    if any(word in query for word in ['failed', 'failure', 'unsuccessful']):
        return "investigate_failures"
    elif any(word in query for word in ['suspicious', 'anomaly', 'threat']):
        return "threat_detection"
    elif 'network' in query or 'connection' in query:
        return "network_analysis"
    elif 'authentication' in query or 'login' in query:
        return "authentication_analysis"
    elif 'system' in query or 'process' in query:
        return "system_analysis"
    else:
        return "general_search"

def extract_entities(query: str) -> Dict[str, Any]:
    """Extract entities from the query"""
    entities = {}
    
    # Extract IP addresses
    ip_matches = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', query)
    if ip_matches:
        entities['ip_addresses'] = ip_matches
    
    # Extract usernames
    user_match = re.search(r'(?:user|username|account)\s+(\w+)', query.lower())
    if user_match:
        entities['username'] = user_match.group(1)
    
    # Extract time references
    time_refs = []
    if 'hour' in query:
        time_refs.append('hour')
    if 'day' in query or 'today' in query:
        time_refs.append('day')
    if 'week' in query:
        time_refs.append('week')
    if 'month' in query:
        time_refs.append('month')
    
    if time_refs:
        entities['time_references'] = time_refs
    
    return entities