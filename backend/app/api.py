"""
FastAPI application for OfficeOS legal research backend.
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import (
    LegalResearchRequest,
    LegalResearchResponse,
    ErrorResponse
)
from app.flows.legal_research import legal_research_flow
from app.services.openai_client import get_openai_service

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="OfficeOS Legal Research Backend",
    description="Prefect-orchestrated legal research workflow for OfficeOS hackathon demo",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Validate environment configuration on startup."""
    logger.info("Starting OfficeOS Legal Research Backend")
    try:
        get_openai_service()
        logger.info("OpenAI service validated successfully")
    except ValueError as e:
        logger.error(f"Startup validation failed: {str(e)}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "OfficeOS Legal Research Backend"}


@app.post(
    "/api/legal-research",
    response_model=LegalResearchResponse,
    responses={
        200: {"model": LegalResearchResponse},
        500: {"model": ErrorResponse}
    }
)
async def legal_research_endpoint(request: LegalResearchRequest) -> LegalResearchResponse:
    """
    Execute legal research workflow.
    
    This endpoint accepts a legal research topic, triggers the Prefect workflow,
    and returns a structured legal briefing.
    
    Args:
        request: LegalResearchRequest containing the research topic
        
    Returns:
        LegalResearchResponse with status, topic, and summarized briefing
        
    Raises:
        HTTPException: If workflow execution fails
    """
    logger.info(f"Legal research request received: {request.topic}")
    
    try:
        # Run the Prefect flow synchronously
        logger.info("Triggering legal_research_flow")
        summary = legal_research_flow(topic=request.topic)
        
        logger.info("Legal research workflow completed successfully")
        
        return LegalResearchResponse(
            status="completed",
            topic=request.topic,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Legal research workflow failed"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )
