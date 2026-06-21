from os import path, getenv
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct
)
import numpy as np
import json

load_dotenv()

QDRANT_URL = getenv("QDRANT_URL")
QDRANT_API_KEY = getenv("QDRANT_API_KEY")

EMBEDDINGS_FILEPATH = path.join("data", "embeddings", "embeddings.npy")
METADATA_FILEPATH = path.join("data", "processed", "chunks.jsonl")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def create_collection(collection_name):
    if client.collection_exists(collection_name):
        print(f"Collection '{collection_name}' already exists.\n\tAborting collection creation.....")
        return
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


def load_points(batch_size=100):
    embeddings = np.load(
        EMBEDDINGS_FILEPATH,
        mmap_mode='r'
    )
    points = []

    with open(METADATA_FILEPATH, 'r') as f:
        for idx, line in enumerate(f):
            metadata = json.loads(line)
            point = PointStruct(
                id=idx,
                vector=embeddings[idx].tolist(),
                payload=metadata
            )
            points.append(point)

            if len(points) == batch_size:
                yield points
                points = []
    
    if points:
        yield points        


def upsert_points(collection_name):
    for points in load_points():
        client.upsert(
            collection_name=collection_name,
            points=points
        )


def main():
    collection_name = "cuda-docs"

    create_collection(collection_name)
    upsert_points(collection_name)


if __name__ == "__main__":
    main()