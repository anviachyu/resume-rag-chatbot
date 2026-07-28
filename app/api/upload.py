from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_reader import extract_text_from_pdf
from app.services.chunker import split_text_into_chunks
from app.services.embeddings import create_embeddings


router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    file_name = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIRECTORY / file_name

    try:
        file_content = await file.read()
        file_path.write_bytes(file_content)

        resume_text = extract_text_from_pdf(file_path)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF.",
            )
        chunks = split_text_into_chunks(resume_text)
        embeddings = create_embeddings(chunks)
        return {
           " message": "Resume uploaded and embedded successfully",
           "file_name": file.filename,
    "characters_extracted": len(resume_text),
    "number_of_chunks": len(chunks),
    "number_of_embeddings": len(embeddings),
    "embedding_dimension": (
        embeddings.shape[1] if len(embeddings) > 0 else 0
        ),
    "first_chunk": chunks[0] if chunks else "",
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to process the resume: {error}",
        ) from error

    finally:
        await file.close()