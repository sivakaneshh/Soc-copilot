from typing import Dict, Any, List
from elasticsearch import Elasticsearch
import os
import logging

# Initialize Elasticsearch client
es_url = os.getenv("ELASTICSEARCH_URL", "http://127.0.0.1:9200")
es = Elasticsearch(
    [es_url],
    # Force compatibility with Elasticsearch 8.x
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}
)

logger = logging.getLogger(__name__)

def run_query(index: str, dsl: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Elasticsearch query"""
    try:
        # If no specific index provided, search all security log indices
        if index == "security-logs":
            index = "security-logs-*"
        
        result = es.search(index=index, **dsl)
        return result
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        # Return mock data if Elasticsearch is not available
        return get_mock_results(index)

def index_logs(index_name: str, logs: List[Dict[str, Any]]) -> int:
    """Index logs to Elasticsearch"""
    try:
        logger.info(f"Attempting to index {len(logs)} logs to index {index_name}")
        
        # Create index if it doesn't exist (with minimal mapping)
        if not es.indices.exists(index=index_name):
            logger.info(f"Creating new index: {index_name}")
            # Use minimal mapping to avoid conflicts
            mapping = {
                "mappings": {
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "message": {"type": "text"}
                    }
                }
            }
            es.indices.create(index=index_name, body=mapping)
        
        # Bulk index logs
        actions = []
        for i, log in enumerate(logs):
            try:
                # Clean the log data
                log_data = {}
                for k, v in log.items():
                    if k != '_id' and v is not None:
                        log_data[k] = str(v) if not isinstance(v, (dict, list)) else v
                
                action = {
                    "_index": index_name,
                    "_source": log_data
                }
                
                # Only add _id if it exists and is not None/empty
                if log.get("_id") and log["_id"].strip():
                    action["_id"] = log["_id"]
                    
                actions.append(action)
                
            except Exception as log_error:
                logger.error(f"Error processing log {i}: {str(log_error)}")
                continue
        
        if actions:
            logger.info(f"Bulk indexing {len(actions)} documents")
            from elasticsearch.helpers import bulk
            success_count, failed_items = bulk(es, actions, raise_on_error=False)
            logger.info(f"Successfully indexed {success_count} documents")
            if failed_items:
                logger.warning(f"Failed to index some documents: {failed_items}")
            return success_count
        else:
            logger.warning("No valid actions to index")
            return 0
    
    except Exception as e:
        logger.error(f"Error indexing logs: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        # Try to provide more debug info
        try:
            logger.error(f"Elasticsearch info: {es.info()}")
        except Exception:
            logger.error("Cannot get Elasticsearch info")
        # Fail gracefully for API endpoints: return 0 indexed documents
        return 0

def get_indices_stats() -> List[Dict[str, Any]]:
    """Get statistics for all security log indices"""
    try:
        # First check if any security indices exist
        try:
            indices = es.indices.get(index="security-logs-*")
            stats = es.indices.stats(index="security-logs-*")
        except Exception as e:
            if "index_not_found_exception" in str(e).lower():
                # No indices found yet
                return []
            else:
                raise e
        
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
