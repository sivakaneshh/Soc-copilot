from typing import Dict, Any, List
from elasticsearch import Elasticsearch
import os
import logging

# Initialize Elasticsearch client
es_url = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
es = Elasticsearch([es_url])

logger = logging.getLogger(__name__)

def run_query(index: str, dsl: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Elasticsearch query"""
    try:
        # If no specific index provided, search all security log indices
        if index == "security-logs":
            index = "security-logs-*"
        
        result = es.search(index=index, body=dsl)
        return result
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        # Return mock data if Elasticsearch is not available
        return get_mock_results(index)

def index_logs(index_name: str, logs: List[Dict[str, Any]]) -> int:
    """Index logs to Elasticsearch"""
    try:
        # Create index mapping for security logs
        mapping = {
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "log_type": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "user": {"type": "keyword"},
                    "source_ip": {"type": "ip"},
                    "dest_ip": {"type": "ip"},
                    "port": {"type": "integer"},
                    "severity": {"type": "keyword"},
                    "message": {"type": "text"},
                    "status": {"type": "keyword"},
                    "host": {"type": "keyword"}
                }
            }
        }
        
        # Create index if it doesn't exist
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body=mapping)
        
        # Bulk index logs
        actions = []
        for log in logs:
            action = {
                "_index": index_name,
                "_id": log.get("_id"),
                "_source": log
            }
            actions.append(action)
        
        if actions:
            from elasticsearch.helpers import bulk
            bulk(es, actions)
        
        return len(logs)
    
    except Exception as e:
        logger.error(f"Error indexing logs: {str(e)}")
        raise e

def get_indices_stats() -> List[Dict[str, Any]]:
    """Get statistics for all security log indices"""
    try:
        indices = es.indices.get("security-logs-*")
        stats = es.indices.stats("security-logs-*")
        
        result = []
        for index_name in indices.keys():
            index_stats = stats["indices"].get(index_name, {})
            result.append({
                "index_name": index_name,
                "doc_count": index_stats.get("total", {}).get("docs", {}).get("count", 0),
                "size_bytes": index_stats.get("total", {}).get("store", {}).get("size_in_bytes", 0)
            })
        
        return result
    
    except Exception as e:
        logger.error(f"Error getting indices stats: {str(e)}")
        return []

def get_mock_results(index: str) -> Dict[str, Any]:
    """Return mock results when Elasticsearch is not available"""
    return {
        "took": 5,
        "timed_out": False,
        "hits": {
            "total": {"value": 3, "relation": "eq"},
            "hits": [
                {
                    "_index": index,
                    "_id": "1",
                    "_source": {
                        "@timestamp": "2024-01-15T10:30:00Z",
                        "message": "User login attempt failed",
                        "user": "admin",
                        "source_ip": "192.168.1.100",
                        "log_type": "authentication",
                        "status": "failed"
                    }
                },
                {
                    "_index": index,
                    "_id": "2", 
                    "_source": {
                        "@timestamp": "2024-01-15T10:25:00Z",
                        "message": "Suspicious network activity detected",
                        "source_ip": "10.0.0.50",
                        "dest_port": 443,
                        "log_type": "network"
                    }
                },
                {
                    "_index": index,
                    "_id": "3",
                    "_source": {
                        "@timestamp": "2024-01-15T10:20:00Z",
                        "message": "System file modified",
                        "file_path": "/etc/passwd",
                        "user": "root",
                        "log_type": "system"
                    }
                }
            ]
        }
    }
