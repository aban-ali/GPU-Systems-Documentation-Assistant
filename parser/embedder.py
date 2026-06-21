from sentence_transformers import SentenceTransformer
from os import path
import json
import numpy as np

INPUT_FILEPATH = path.join("data", "processed", "chunks.jsonl")
OUTPUT_EMBEDDINGS = path.join("data", "embeddings", "embeddings.npy")

def create_embeddings(model):
    texts = []

    with open(INPUT_FILEPATH, "r") as f:
        for line in f:
            chunk = json.loads(line)
            texts.append(chunk["chunk"])

    embeddings = model.encode(
        texts,
        batch_size = 32,    #can be adjusted based on available GPU memory
        convert_to_numpy = True,
        show_progress_bar = True
    )

    embeddings = embeddings.astype(np.float32)
    print(f"Embeddings shape: {embeddings.shape}")

    np.save(
        OUTPUT_EMBEDDINGS,
        embeddings
    )

if __name__ == "__main__":
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    create_embeddings(model)