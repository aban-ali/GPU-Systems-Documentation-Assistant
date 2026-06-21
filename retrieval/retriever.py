from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from os import getenv
import numpy as np
import dotenv

dotenv.load_dotenv()

QDRANT_URL = getenv("QDRANT_URL")
QDRANT_API_KEY = getenv("QDRANT_API_KEY")


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        self.collection_name = "cuda-docs"

    def search(self, query, k=5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype(np.float32)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding[0],
            limit=k,
            with_payload=True
        )
        return results


if __name__ == "__main__":

    retriever = Retriever()
    query = "When does bank conflict happen in shared memory?"
    results = retriever.search(query)
    for r in results.points:
        print("\n")
        print("=" * 80)
        print(
            f"{r.payload['source']} | "
            f"page {r.payload['chunk_id']} | "
            f"score={r.score:.4f}"
        )
        print("\n")
        print(r.payload["text"])