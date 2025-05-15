from pydantic import BaseModel, Field
from typing import Optional

class UserQuery(BaseModel):
    """Model for user legal query."""
    query: str = Field(
        ..., 
        min_length=1, 
        description="Legal question or case description"
    )

class LawResponse(BaseModel):
    """Model for legal response."""
    law: Optional[str] = None
    error: Optional[str] = None
