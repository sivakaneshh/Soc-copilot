from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
def generate_report():
    # Logic to generate the report
    return {"status": "report generated","download_link": "/mock/report.pdf"}