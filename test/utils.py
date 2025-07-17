from fastapi.testclient import TestClient
from store.store import SESSION_STORE, CHAT_STORE
from app import app
from models.chat_model import ChatModel, Role
from models.session_model import SessionModel
import pytest

client = TestClient(app=app)

'''
    Sets up a simple session
'''
@pytest.fixture()
def setup_store():
    SESSION_STORE.append(
        SessionModel(session_id=1, 
                     session_user="helloworld", 
                     created_at="",
                     )
    )
    CHAT_STORE[1] = [
        ChatModel(
        role=Role.ASSISTANT,
        content="How may I help you?"
    ),
    ChatModel(
        role=Role.USER,
        content="What is the weather like in London?"
    )
    ]


'''
    Cleans up in-memory store post a test
'''
@pytest.fixture()
def clean_store():
    yield

    SESSION_STORE.clear()
    CHAT_STORE.clear()