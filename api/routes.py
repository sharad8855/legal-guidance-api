from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from db.models import UserQuery, LawResponse
from services.llm import llm_service
from config import logger

# Create router
router = APIRouter()


# Main endpoint - legal query processing
@router.post("/get_law", response_model=LawResponse)
async def get_law(user_query: UserQuery):
    """Process a legal query and return a response."""
    try:
        if len(user_query.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )

        logger.info(f"Received query: {user_query.query}")
        
        # Generate response using LLM service
        answer = await llm_service.generate_response(user_query.query)
        
        logger.info("Successfully processed response")
        return LawResponse(law=answer)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
