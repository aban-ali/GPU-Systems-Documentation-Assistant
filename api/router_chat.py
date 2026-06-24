from fastapi import APIRouter, Depends

from api.schemas import QueryRequest, QueryResponse
from api.dependencies import get_llm, get_retriever

router = APIRouter(
    prefix="/llm", tags=["LLM", "RAG"]
)

@router.post("/chat", response_model=QueryResponse)
async def chat(
    query_request: QueryRequest,
    retriever = Depends(get_retriever),
    llm = Depends(get_llm)
    ):

    query = query_request.query
    top_k = query_request.top_k

    retrieved_docs = retriever.search(query, top_k)
    text = retriever.build_text(retrieved_docs)
    response = llm.generate(query, text)

    return QueryResponse(
        response=response
    )