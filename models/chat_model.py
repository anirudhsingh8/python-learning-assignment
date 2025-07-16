from enum import Enum

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatModel:
    role: Role
    content: str

    def __init__(self, role: Role, content: str):
        self.role = role
        self.content = content