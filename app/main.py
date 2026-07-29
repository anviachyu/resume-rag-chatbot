from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.search import router as search_router


app = FastAPI(
    title="Resume RAG Chatbot",
    description="Upload a resume and ask questions about the candidate.",
    version="1.0.0",
)

app.include_router(upload_router)
app.include_router(search_router)


@app.get("/")
def home():
    return {
        "message": "Resume RAG Chatbot API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}