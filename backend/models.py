"""Pydantic data models for LegalEase API."""

from typing import Optional
from pydantic import BaseModel, Field


class LegalRequest(BaseModel):
    """Request model for legal query."""
    question: str = Field(
        ...,
        min_length=1,
        description="The legal question or inquiry from the user.",
        examples=["What is the difference between a breach of contract and negligence?"]
    )
    context: Optional[str] = Field(
        default=None,
        description="Optional additional context such as jurisdiction, background, or factual circumstances.",
        examples=["Jurisdiction: California, USA"]
    )


class LegalResponse(BaseModel):
    """Response model returning AI-generated legal information and disclaimer."""
    answer: str = Field(
        ...,
        description="AI-generated legal information and analysis."
    )
    disclaimer: str = Field(
        ...,
        description="Standard legal disclaimer emphasizing that information is not professional legal advice."
    )


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(default="healthy", description="Current service health status.")
    service: str = Field(default="LegalEase Backend", description="Service name.")
    version: str = Field(default="1.0.0", description="API version.")
