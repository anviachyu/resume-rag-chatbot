# Resume RAG Chatbot

A Resume Retrieval-Augmented Generation (RAG) chatbot built with Python and FastAPI. Users can upload a resume in PDF format, extract its content, and eventually ask questions about the candidate’s experience, projects, education, and technical skills.

## Current Features

- FastAPI backend
- Health-check endpoint
- PDF resume upload
- PDF text extraction
- File-type validation
- Automatic API documentation
- Secure handling of uploaded resumes

## Planned Features

- Resume text chunking
- Sentence-transformer embeddings
- FAISS vector storage
- Semantic resume search
- LLM-powered question answering
- Source-grounded responses
- Streamlit recruiter interface
- Automated tests and Docker deployment

## Technology Stack

- Python
- FastAPI
- Uvicorn
- PyPDF
- LangChain
- Sentence Transformers
- FAISS
- Streamlit

## Project Structure

```text
resume-rag-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── upload.py
│   └── services/
│       ├── __init__.py
│       └── pdf_reader.py
├── uploads/
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/resume-rag-chatbot.git
cd resume-rag-chatbot
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

### 5. Open the API documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Confirms that the API is running |
| GET | `/health` | Returns application health |
| POST | `/resume/upload` | Uploads a PDF resume and extracts its text |

## Testing the Upload Endpoint

1. Open `http://127.0.0.1:8000/docs`.
2. Expand `POST /resume/upload`.
3. Click **Try it out**.
4. Choose a PDF resume.
5. Click **Execute**.
6. Review the extracted-text preview in the response.

## Privacy

Uploaded resumes, PDF files, environment variables, and virtual-environment files are excluded from Git using `.gitignore`.

## Project Status

This project is under active development. The next milestone is splitting resume content into chunks and storing their embeddings in FAISS.

## Author

**Naga Venkata Anvitha**  
AI/ML Engineer
