from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from api.routes import router
from config import logger

# FastAPI app initialization
app = FastAPI(
    title="Legal Information API",
    description="API to get legal information using Gemini AI",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:9000",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:9000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include API routes
app.include_router(router)

# Mount static files
try:
    # Get the directory path for the templates
    current_dir = os.path.dirname(os.path.dirname(__file__))
    templates_dir = os.path.join(current_dir, "templates")
    
    # Check if the templates directory exists
    if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
        app.mount("/static", StaticFiles(directory=templates_dir), name="static")
        logger.info(f"Mounted static files from {templates_dir}")
    else:
        logger.warning(f"Templates directory not found at {templates_dir}")
except Exception as e:
    logger.error(f"Error mounting static files: {str(e)}")

# Run the app
if __name__ == "__main__":
    logger.info("Starting Legal Information API")
    uvicorn.run(app, host="0.0.0.0", port=9000)
