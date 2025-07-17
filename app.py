from fastapi import FastAPI, HTTPException, status
from dtos.create_session_request import CreateSessionRequest
from dtos.create_chat_request import CreateChatRequest
from store.store import SESSION_STORE, CHAT_STORE
from models.session_model import SessionModel
from models.chat_model import Role
from utils import *
from typing import Optional

app = FastAPI()


@app.post("/sessions/", status_code=status.HTTP_201_CREATED)
def create_session(session: CreateSessionRequest):
    username = clean_username(session.session_user)
    session_id = len(SESSION_STORE) + 1
    created_at = get_current_utc_timestamp()

    session = SessionModel(
        session_id=session_id,
        session_user=username,
        created_at=created_at,
    )

    SESSION_STORE.append(session)
    # Assuming we are allowing duplicate usernames
    CHAT_STORE[session_id] = []

    return session


@app.get("/sessions/{session_id}/messages/", status_code=status.HTTP_200_OK)
def get_chats(session_id: int, role: Optional[Role] = None):
    if CHAT_STORE.get(session_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found!",
        )

    chats = CHAT_STORE[session_id]

    if role != None:
        return [chat for chat in chats if chat.role == role]

    return chats


@app.post("/sessions/{session_id}/messages/", status_code=status.HTTP_201_CREATED)
def create_chat(session_id: int, chat: CreateChatRequest):
    if CHAT_STORE.get(session_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found!",
        )

    CHAT_STORE[session_id].append(chat)
    return {"message": "success"}
