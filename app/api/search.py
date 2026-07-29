from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.embeddings import create_embeddings
from app.services.vector_store import search_vector_store


router = APIRouter(prefix="/resume", tags=["Resume"])


class SearchRequest(BaseModel):
    question: str = Field(min_length=2)
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("/search")
def search_resume(request: SearchRequest):
    try:
        query_embedding = create_embeddings([request.question])

        results = search_vector_store(
            query_embedding=query_embedding,
            top_k=request.top_k,
        )

        return {
            "question": request.question,
            "number_of_results": len(results),
            "results": results,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to search the resume: {error}",
        ) from error