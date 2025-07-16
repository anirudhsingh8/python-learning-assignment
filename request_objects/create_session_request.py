from pydantic import BaseModel, Field

class CreateSessionRequest(BaseModel):
    session_user: str = Field(..., min_length=1)