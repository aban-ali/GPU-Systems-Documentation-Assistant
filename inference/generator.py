import torch
from transformers import pipeline

from inference.prompts import RAG_SYSTEM_PROMPT

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

class Generator:
    def __init__(self, model_id: str = "meta-llama/Llama-3.2-1B-Instruct"):
        self.model_id = model_id
        self.pipe = pipeline(
            "text-generation",
            model=self.model_id,
            dtype=torch.bfloat16,
            device_map="auto",
        )

    def generate(
            self, query: str, retrieved_doc: str = "",
            max_new_tokens: int = 1024
            ):
        messages = [
            {"role": "system", "content": RAG_SYSTEM_PROMPT.format(retrieved_docs=retrieved_doc)},
            {"role": "user", "content": query}
        ]
        output = self.pipe(
            messages, max_new_tokens=max_new_tokens,
            temperature=0.7, top_p=0.9
        )
        
        return output[0]['generated_text'][-1]['content']