from fastapi import FastAPI
from pydantic import BaseModel

from src.rag.qa_chain import answer


class AskRequest(BaseModel):
    query: str


class Source(BaseModel):
    text: str
    metadata: dict


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


app = FastAPI(title="docqa-portal API")


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    ans, docs = answer(req.query)
    return AskResponse(
        answer=ans,
        sources=[Source(**d) for d in docs],
    )