from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class NLQuery(BaseModel):
    user_id: str
    query: str

@router.post("/")

def converse(query: NLQuery):
    return{
        "dsl" : {"mock": "dsl_query"},
        "explanation": "Translated '{query.query}' to DSL",
        "result": {"sample": "result"}
    }
