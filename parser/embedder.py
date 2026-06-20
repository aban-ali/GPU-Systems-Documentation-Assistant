from sentence_transformers import SentenceTransformer
from os import path
import json
import numpy as np

INPUT_FILEPATH = path.join("data", "processed", "chunks.jsonl")
OUTPUT_EMBEDDINGS = path.join("data", "embeddings", "embeddings.npy")
OUTPUT_MAPPINGS = path.join("data", "embeddings", "idx_to_chunk.json")

def create_embeddings(model):
    texts = []
    idx_to_chunk = {}

    with open(INPUT_FILEPATH, "r") as f:
        for idx, line in enumerate(f):
            chunk = json.loads(line)
            texts.append(chunk["chunk"])
            idx_to_chunk[idx] = chunk
    
    embeddings = model.encode(
        texts,
        batch_size = 32,
        convert_to_numpy = True,
        show_progress_bar = True
    )

    embeddings = embeddings.astype(np.float32)
    print(f"Embeddings shape: {embeddings.shape}")

    np.save(
        OUTPUT_EMBEDDINGS,
        embeddings
    )

    with open(OUTPUT_MAPPINGS, "w") as f:
        json.dump(idx_to_chunk, f)

if __name__ == "__main__":
    model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
    create_embeddings(model)