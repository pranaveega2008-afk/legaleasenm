"""Gemini AI Service integration for LegalEase."""

import os
from typing import Optional, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Load environment variables from .env file
load_dotenv(override=True)

# System instruction guiding the AI behavior and ethical boundaries
LEGAL_SYSTEM_INSTRUCTION = (
    "You are LegalEase, an AI-powered legal information assistant. "
    "Your objective is to help everyday people and businesses understand legal concepts clearly.\n\n"
    "Strict Operational Guidelines:\n"
    "1. General Information Only: Provide objective, educational legal information. "
    "You are NOT an attorney, law firm, or legal counsel. Never pretend to be a lawyer or establish an attorney-client relationship.\n"
    "2. Plain Language: Explain complex legal jargon, doctrines, and concepts in simple, accessible, easy-to-understand language.\n"
    "3. No Hallucinations: Never invent or hallucinate statutes, precedents, citations, court cases, or legal rules. If a statute or precedent is uncertain, explicitly state that you cannot confirm specific citations.\n"
    "4. Explicit Uncertainty: Acknowledge ambiguities, gray areas, and uncertainties in the law.\n"
    "5. Jurisdiction Awareness: Always advise the user that legal rules vary substantially across jurisdictions (national, state/provincial, and local levels) and ask them to verify jurisdiction-specific rules.\n"
    "6. No Illegal Assistance: Strictly refuse to encourage, assist, facilitate, or advise on illegal activities or how to circumvent the law.\n"
    "7. Structured Formatting: Organize responses with clear markdown headings, bullet points, concise paragraphs, and bold key terms for readability.\n"
    "8. Prominent Professional Advice Reminder: Conclude or include a clear reminder that your response is general informational material and not a substitute for qualified legal advice from an attorney licensed in the relevant jurisdiction."
)

DEFAULT_LEGAL_DISCLAIMER = (
    "IMPORTANT DISCLAIMER: LegalEase provides general legal information for educational "
    "and informational purposes only. It is NOT legal advice and does NOT create an "
    "attorney-client relationship. Laws vary significantly across jurisdictions and change frequently. "
    "You should not rely on this information as a substitute for professional advice from a licensed attorney "
    "in your jurisdiction."
)


def get_gemini_api_key() -> str:
    """Retrieve and validate the Gemini API key from environment."""
    # Ensure fresh load of environment variables in case .env was updated
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    return api_key


def generate_legal_response(question: str, context: Optional[str] = None) -> Tuple[str, str]:
    """
    Generate a structured legal information response using Google Gemini API.

    Args:
        question: User's legal question.
        context: Optional additional context (jurisdiction, facts, background).

    Returns:
        Tuple of (answer_text, disclaimer_text)

    Raises:
        ValueError: If question is empty or Gemini API key is missing/unconfigured.
        APIError: If the Gemini API returns an error.
        Exception: For other unexpected failures.
    """
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        raise ValueError("Question cannot be empty or whitespace only.")

    api_key = get_gemini_api_key()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "Gemini API key is not configured. Please set a valid GEMINI_API_KEY in the .env file."
        )

    # Initialize Google GenAI client
    client = genai.Client(api_key=api_key)

    # Prepare user query with optional context
    prompt_parts = []
    if context and context.strip():
        prompt_parts.append(f"Additional Context / Jurisdiction:\n{context.strip()}\n")
    prompt_parts.append(f"Legal Question:\n{cleaned_question}")

    user_prompt = "\n".join(prompt_parts)

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Generate content using Gemini Flash
    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=LEGAL_SYSTEM_INSTRUCTION,
            temperature=0.3,
        ),
    )

    answer_text = response.text or "No response could be generated."
    return answer_text, DEFAULT_LEGAL_DISCLAIMER
