import json
from pathlib import Path

import faiss
import numpy as np


VECTOR_STORE_DIRECTORY = Path("vector_store")
INDEX_PATH = VECTOR_STORE_DIRECTORY / "resume.index"
CHUNKS_PATH = VECTOR_STORE_DIRECTORY / "chunks.json"


def save_vector_store(
    embeddings: np.ndarray,
    chunks: list[str],
) -> int:
    """
    Store resume embeddings in FAISS and save the corresponding
    resume chunks in a JSON file.
    """
    if embeddings.size == 0 or not chunks:
        raise ValueError("Embeddings and chunks cannot be empty.")

    if len(embeddings) != len(chunks):
        raise ValueError(
            "The number of embeddings must match the number of chunks."
        )

    VECTOR_STORE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    embeddings = np.ascontiguousarray(
        embeddings,
        dtype="float32",
    )

    dimension = embeddings.shape[1]

    # IndexFlatIP performs inner-product similarity search.
    # Because the embeddings are normalized, this behaves
    # like cosine similarity.
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with CHUNKS_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return index.ntotal


def search_vector_store(
    query_embedding: np.ndarray,
    top_k: int = 3,
) -> list[dict]:
    """
    Search FAISS and return the resume chunks that are most
    relevant to the user's question.
    """
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "No resume vector store exists. Upload a resume first."
        )

    if query_embedding.size == 0:
        raise ValueError("Query embedding cannot be empty.")

    index = faiss.read_index(str(INDEX_PATH))

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    query_embedding = np.ascontiguousarray(
        query_embedding,
        dtype="float32",
    )

    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    if query_embedding.shape[1] != index.d:
        raise ValueError(
            "The query embedding dimension does not match "
            "the FAISS index dimension."
        )

    number_of_results = min(top_k, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        number_of_results,
    )

    results = []

    for score, chunk_index in zip(scores[0], indices[0]):
        if chunk_index == -1:
            continue

        results.append(
            {
                "chunk": chunks[chunk_index],
                "similarity_score": round(float(score), 4),
            }
        )

    return results