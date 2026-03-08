"""
Main entry point for OfficeOS Legal Research Backend.

Start the server with:
    uvicorn main:app --reload

For production:
    uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Loading OfficeOS Legal Research Backend")

# Import FastAPI app
from app.api import app

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port} (reload={reload})")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
