from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import csv
import io
from datetime import datetime, timezone
from app.core.elastic_client import index_logs, get_indices_stats
import uuid

router = APIRouter()

class LogUploadResponse(BaseModel):
    success: bool
    message: str
    indexed_count: int
    index_name: str

class IndexInfo(BaseModel):
    index_name: str
    doc_count: int
    size_bytes: int

@router.post("/upload", response_model=LogUploadResponse)
async def upload_logs(file: UploadFile = File(...)):
    """Upload security logs from JSON or CSV file"""
    try:
        # Generate unique index name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index_name = f"security-logs-{timestamp}"
        
        content = await file.read()
        
        # Parse file based on extension
        if file.filename.endswith('.json'):
            logs = parse_json_logs(content)
        elif file.filename.endswith('.csv'):
            logs = parse_csv_logs(content)
        else:
            raise HTTPException(status_code=400, detail="Only JSON and CSV files are supported")
        
        # Index logs to Elasticsearch
        indexed_count = index_logs(index_name, logs)
        
        return LogUploadResponse(
            success=True,
            message=f"Successfully uploaded {indexed_count} logs to index '{index_name}'",
            indexed_count=indexed_count,
            index_name=index_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading logs: {str(e)}")

@router.get("/indices", response_model=List[IndexInfo])
def get_log_indices():
    """Get all available log indices"""
    try:
        return get_indices_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching indices: {str(e)}")

@router.post("/sample-data")
def create_sample_data():
    """Create sample security logs for demonstration"""
    try:
        sample_logs = generate_sample_logs()
        index_name = f"security-logs-sample-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        indexed_count = index_logs(index_name, sample_logs)
        
        return {
            "success": True,
            "message": f"Created {indexed_count} sample logs in index '{index_name}'",
            "indexed_count": indexed_count,
            "index_name": index_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sample data: {str(e)}")

def parse_json_logs(content: bytes) -> List[Dict[str, Any]]:
    """Parse JSON logs from uploaded file"""
    try:
        text_content = content.decode('utf-8')
        # Try to parse as JSON array first
        try:
            logs = json.loads(text_content)
            if isinstance(logs, list):
                return [normalize_log(log) for log in logs]
            else:
                return [normalize_log(logs)]
        except json.JSONDecodeError:
            # Try to parse as JSONL (one JSON per line)
            logs = []
            for line in text_content.strip().split('\n'):
                if line.strip():
                    logs.append(normalize_log(json.loads(line)))
            return logs
    except Exception as e:
        raise ValueError(f"Error parsing JSON: {str(e)}")

def parse_csv_logs(content: bytes) -> List[Dict[str, Any]]:
    """Parse CSV logs from uploaded file"""
    try:
        text_content = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(text_content))
        return [normalize_log(row) for row in csv_reader]
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def normalize_log(log: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize log entry with required fields"""
    normalized = dict(log)
    
    # Ensure timestamp field
    if '@timestamp' not in normalized:
        if 'timestamp' in normalized:
            normalized['@timestamp'] = normalized['timestamp']
        elif 'time' in normalized:
            normalized['@timestamp'] = normalized['time']
        else:
            normalized['@timestamp'] = datetime.now(timezone.utc).isoformat()
    
    # Ensure ID field
    if '_id' not in normalized:
        normalized['_id'] = str(uuid.uuid4())
    
    # Add log type if not present
    if 'log_type' not in normalized:
        normalized['log_type'] = 'security'
    
    return normalized

def generate_sample_logs() -> List[Dict[str, Any]]:
    """Generate realistic sample security logs"""
    import random
    from datetime import timedelta
    
    base_time = datetime.now(timezone.utc)
    sample_logs = []
    
    # Authentication logs
    for i in range(50):
        timestamp = base_time - timedelta(hours=random.randint(0, 72))
        success = random.choice([True, False])
        
        log = {
            "_id": str(uuid.uuid4()),
            "@timestamp": timestamp.isoformat(),
            "log_type": "authentication",
            "event_type": "login_attempt",
            "user": f"user{random.randint(1, 20)}",
            "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "status": "success" if success else "failed",
            "message": f"User login {'successful' if success else 'failed'}",
            "severity": "info" if success else "warning",
            "service": "ssh"
        }
        sample_logs.append(log)
    
    # Network logs
    for i in range(30):
        timestamp = base_time - timedelta(hours=random.randint(0, 72))
        
        log = {
            "_id": str(uuid.uuid4()),
            "@timestamp": timestamp.isoformat(),
            "log_type": "network",
            "event_type": "connection",
            "source_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "dest_ip": f"203.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "port": random.choice([80, 443, 22, 3389, 8080]),
            "protocol": random.choice(["TCP", "UDP"]),
            "bytes_in": random.randint(1000, 50000),
            "bytes_out": random.randint(500, 25000),
            "message": "Network connection established",
            "severity": "info"
        }
        sample_logs.append(log)
    
    # System logs
    for i in range(20):
        timestamp = base_time - timedelta(hours=random.randint(0, 72))
        
        log = {
            "_id": str(uuid.uuid4()),
            "@timestamp": timestamp.isoformat(),
            "log_type": "system",
            "event_type": random.choice(["process_start", "file_access", "service_start"]),
            "host": f"server{random.randint(1, 5)}",
            "process": random.choice(["apache2", "nginx", "sshd", "systemd", "cron"]),
            "message": f"System event occurred",
            "severity": random.choice(["info", "warning", "error"])
        }
        sample_logs.append(log)
    
    return sample_logs