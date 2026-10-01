"""FastAPI application for LegalEase backend."""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import APIError

from backend.models import LegalRequest, LegalResponse, HealthResponse
from backend.gemini_service import generate_legal_response

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LegalEaseAPI")

# Initialize FastAPI application
app = FastAPI(
    title="⚖️ LegalEase API",
    description="Backend REST API providing AI-driven legal information powered by Google Gemini.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend clients (e.g. Streamlit, web browsers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
async def root():
    """Root endpoint welcoming users and pointing to API documentation."""
    return {
        "message": "Welcome to the LegalEase API",
        "service": "LegalEase",
        "status": "active",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify backend service availability."""
    return HealthResponse(
        status="healthy",
        service="LegalEase Backend",
        version="1.0.0",
    )


@app.post(
    "/ask",
    response_model=LegalResponse,
    status_code=status.HTTP_200_OK,
    tags=["Legal Assistant"],
    summary="Get legal information and guidance for a query",
)
async def ask_legal_question(request: LegalRequest):
    """
    Process a legal question and return AI-generated legal information with disclaimers.

    - **question**: The legal inquiry or concept to be clarified.
    - **context**: (Optional) Additional background facts or jurisdiction specifications.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'question' field cannot be empty or blank.",
        )

    logger.info(f"Received legal question: {request.question[:80]}...")

    try:
        answer, disclaimer = generate_legal_response(
            question=request.question,
            context=request.context,
        )
        return LegalResponse(answer=answer, disclaimer=disclaimer)

    except ValueError as ve:
        logger.warning(f"Validation / Configuration error: {ve}")
        # Missing API key or configuration error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ve),
        )

    except APIError as api_err:
        logger.error(f"Google Gemini API error: {api_err}")
        err_msg = getattr(api_err, "message", str(api_err))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini API error: {err_msg}",
        )

    except Exception as exc:
        logger.error(f"Unexpected error in /ask: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process legal inquiry: {str(exc)}",
        )
