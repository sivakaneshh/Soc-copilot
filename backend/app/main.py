from fastapi import FastAPI
from app.api import converse, reports

app = FastAPI(title="SOC Bud")

app.include_router(converse.router, prefix="/converse", tags=["converse"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("health")

def health():
    return {"status": "ok"}