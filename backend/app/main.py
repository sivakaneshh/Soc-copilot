from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import converse, reports, logs

app = FastAPI(title="SOC Copilot", description="AI-powered Security Operations Center Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(converse.router, prefix="/converse", tags=["converse"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])

@app.get("/health")
def health():
    return {"status": "ok", "message": "SOC Copilot API is running"}