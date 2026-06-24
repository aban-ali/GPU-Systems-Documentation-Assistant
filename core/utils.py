from contextlib import asynccontextmanager

from retrieval.retriever import Retriever
from inference.generator import Generator


@asynccontextmanager
async def lifespan(app):
    # Initialize the retriever
    app.state.retriever = Retriever()
    # Initialize the generator
    app.state.llm = Generator()

    yield
    
    # cleanup tasks
