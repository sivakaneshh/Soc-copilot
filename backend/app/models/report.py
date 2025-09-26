from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ReportRequest(BaseModel):
    user_id: str
    query_ids: List[str]
    report_type: Optional[str] = "standard"
    title: Optional[str] = None

class ReportResponse(BaseModel):
    report_id: str
    status: str
    download_link: Optional[str] = None
    created_at: datetime
    file_size: Optional[int] = None