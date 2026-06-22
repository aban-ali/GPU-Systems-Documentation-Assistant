from fastapi import Request

def get_retriever(request: Request):
    """
    Dependency function to retrieve the retriever from the request state.
    """
    return request.app.state.retriever

def get_llm(request: Request):
    """
    Dependency function to retrieve the LLM from the request state.
    """
    return request.app.state.llm