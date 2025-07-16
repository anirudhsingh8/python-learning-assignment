from pydantic import BaseModel, Field
from models.chat_model import Role

class CreateChatRequest(BaseModel):
    role: Role
    content: str = Field(..., min_length=1)