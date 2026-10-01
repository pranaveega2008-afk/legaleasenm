"""
backend.py - FastAPI Backend for LegalEase AI Document Generator
Handles Gemini AI integration, legal document generation, and export endpoints.
"""

import os
import io
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Import exporters and fallback templates
from document_templates import build_legal_document, DOCUMENT_TYPES
from pdf_exporter import create_pdf_from_text
from docx_exporter import create_docx_from_text

# Initialize FastAPI App
app = FastAPI(
    title="LegalEase API",
    description="FastAPI Backend for AI Legal Document Generation",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Request Models
class DocumentRequest(BaseModel):
    doc_type: str
    language: str = "en"  # "en" or "ta"
    party1_name: str
    party1_address: str
    party2_name: str
    party2_address: str
    requirements: str
    date: Optional[str] = None
    jurisdiction: Optional[str] = "Chennai, Tamil Nadu"
    extra_terms: Optional[str] = ""
    # Optional specific fields
    rent_amount: Optional[str] = None
    deposit_amount: Optional[str] = None
    duration_months: Optional[str] = None
    notice_period_months: Optional[str] = None
    property_address: Optional[str] = None
    nda_purpose: Optional[str] = None
    nda_period: Optional[str] = None
    service_scope: Optional[str] = None
    service_fee: Optional[str] = None
    service_deadline: Optional[str] = None
    job_title: Optional[str] = None
    annual_ctc: Optional[str] = None
    probation_months: Optional[str] = None
    joining_date: Optional[str] = None
    loan_amount: Optional[str] = None
    interest_rate: Optional[str] = None
    deponent_parent_spouse: Optional[str] = None
    deponent_age: Optional[str] = None
    affidavit_purpose: Optional[str] = None
    affidavit_statement: Optional[str] = None


class ExportRequest(BaseModel):
    title: str
    content: str
    language: str = "en"


def generate_with_gemini(data: DocumentRequest) -> Optional[str]:
    """
    Calls Google Gemini AI to draft a comprehensive, legally sound document.
    Supports both google-genai and google.generativeai libraries.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return None

    # Construct AI Prompt
    lang_name = "TAMIL (தமிழ்)" if data.language == "ta" else "ENGLISH"
    
    prompt = f"""
You are an expert bilingual Indian legal drafting attorney and conveyancing advocate.
Draft a complete, formal, highly professional legal document in {lang_name}.

DOCUMENT TYPE: {data.doc_type}
LANGUAGE: {lang_name}
DATE OF EXECUTION: {data.date or 'Current Date'}
JURISDICTION: {data.jurisdiction or 'Chennai, Tamil Nadu'}

PARTIES:
- First Party (Party 1): {data.party1_name}, Residing / Located at: {data.party1_address}
- Second Party (Party 2): {data.party2_name}, Residing / Located at: {data.party2_address}

LEGAL REQUIREMENTS & SPECIFIC DETAILS:
{data.requirements}

ADDITIONAL TERMS / CUSTOM CLAUSES:
{data.extra_terms or 'None'}

FORMATTING & DRAFTING INSTRUCTIONS:
1. Include a formal legal header and document title in {lang_name}.
2. State the execution date, place/jurisdiction, and full description of both parties.
3. Include formal Recitals ("WHEREAS..."), Definitions, and Numbered Operative Clauses.
4. Incorporate all specific financial numbers, amounts, dates, and duties provided above.
5. Include standard clauses for Governing Law, Dispute Resolution, Severability, and Termination.
6. For TAMIL: Use authentic formal legal conveyancing terminology (e.g., வாடகை ஒப்பந்தம், முதல் தரப்பினர், இரண்டாம் தரப்பினர், விதிமுறைகள் மற்றும் நிபந்தனைகள், சாட்சிகள்).
7. Conclude with complete Execution Signatures (Party 1 and Party 2) and Two Witness Signature lines.
8. Output ONLY the plain text legal document without conversational filler or markdown backtick wrappers.
"""

    # Try new google-genai SDK first
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e1:
        # Fallback to google.generativeai if installed
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e2:
            print(f"[Gemini API Error] {e1} / {e2}")
            return None

    return None


@app.get("/")
def read_root():
    return {
        "app": "LegalEase API",
        "status": "Online",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/api/health")
def health_check():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    has_gemini = bool(api_key and api_key != "your_gemini_api_key_here")
    return {
        "status": "healthy",
        "gemini_configured": has_gemini,
        "supported_documents": list(DOCUMENT_TYPES.keys())
    }


@app.post("/api/generate")
def generate_document_endpoint(request: DocumentRequest):
    """
    Generates a legal document using Gemini AI if configured,
    or falls back to high-precision built-in legal templates.
    """
    source = "gemini_ai"
    generated_text = generate_with_gemini(request)

    # Fallback to local legal templates if Gemini is not configured or fails
    if not generated_text:
        source = "local_template_engine"
        data_dict = request.model_dump()
        generated_text = build_legal_document(
            doc_type=request.doc_type,
            data=data_dict,
            lang=request.language
        )

    title_info = DOCUMENT_TYPES.get(request.doc_type, {"en": request.doc_type, "ta": request.doc_type})
    doc_title = title_info["ta"] if request.language == "ta" else title_info["en"]

    return {
        "success": True,
        "title": doc_title,
        "document": generated_text,
        "source": source,
        "language": request.language,
        "doc_type": request.doc_type
    }


@app.post("/api/export/pdf")
def export_pdf_endpoint(request: ExportRequest):
    """Generates and streams a downloadable PDF file."""
    try:
        pdf_buffer = create_pdf_from_text(
            title=request.title,
            text_content=request.content,
            language=request.language
        )
        filename = f"{request.title.replace(' ', '_')}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_buffer.getvalue()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@app.post("/api/export/docx")
def export_docx_endpoint(request: ExportRequest):
    """Generates and streams a downloadable DOCX file."""
    try:
        docx_buffer = create_docx_from_text(
            title=request.title,
            text_content=request.content,
            language=request.language
        )
        filename = f"{request.title.replace(' ', '_')}.docx"
        return StreamingResponse(
            io.BytesIO(docx_buffer.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate DOCX: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
