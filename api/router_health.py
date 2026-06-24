from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def read_root():
    return {"message": "Service is healthy!"}
