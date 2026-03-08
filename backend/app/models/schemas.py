from pydantic import BaseModel, Field


class LegalResearchRequest(BaseModel):
    """Request model for legal research workflow."""
    topic: str = Field(..., min_length=1, description="The legal research topic or question")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Legal risks of supplier contracts for a hardware startup"
            }
        }


class LegalResearchResponse(BaseModel):
    """Response model for legal research workflow."""
    status: str = Field(..., description="Status of the request (completed or error)")
    topic: str = Field(..., description="The legal research topic")
    summary: str = Field(..., description="The generated legal briefing summary")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "topic": "Legal risks of supplier contracts for a hardware startup",
                "summary": "Key Issue: Risk allocation in supplier agreements\n\nPotential Risk: Lack of clear indemnification clauses could expose the startup to supplier-related liabilities\n\nRecommended Action: Include comprehensive indemnification and limitation of liability provisions in supplier contracts"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    status: str = Field(default="error", description="Status indicating an error occurred")
    message: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "OpenAI API key not configured"
            }
        }
