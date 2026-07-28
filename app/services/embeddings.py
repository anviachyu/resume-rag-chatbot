import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_embedding_model = SentenceTransformer(MODEL_NAME)


def create_embeddings(chunks: list[str]) -> np.ndarray:
    if not chunks:
        return np.empty((0, 384), dtype="float32")

    embeddings = _embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.astype("float32")