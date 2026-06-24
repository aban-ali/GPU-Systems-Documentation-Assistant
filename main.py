from fastapi import FastAPI

from core.utils import lifespan
from core.logger import setup_logger

from api.router_chat import router as chat_router
from api.router_health import router as health_router

logger = setup_logger("root")

logger.info("Initializing app....")
app = FastAPI(
    lifespan=lifespan
)

logger.info("Attaching LLM router.")
app.include_router(
    router=chat_router
)
logger.info("Attaching Health router.")
app.include_router(
    router=health_router
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)