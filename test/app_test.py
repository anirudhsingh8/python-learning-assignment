import pytest
from .utils import client, clean_store, setup_store
from models.chat_model import ChatModel, Role
from store.store import SESSION_STORE, CHAT_STORE
from fastapi import status

def test_create_session_returns_201_on_valid_data(clean_store):
    body = {
        'session_user': 'sample_username'
    }

    res = client.post('/sessions/', json=body)
    
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()['session_id'] == 1
    assert res.json()['session_user'] == 'sample_username'

    # Updates session list
    assert SESSION_STORE[0].session_id == 1
    assert SESSION_STORE[0].session_user == "sample_username"

    # Updates chat map
    assert CHAT_STORE[1] == []

def test_create_session_normalizes_data_before_saving(clean_store):
    body = {
        'session_user': '  sAmple_usernAme  '
    }

    res = client.post('/sessions/', json=body)
    
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()['session_id'] == 1
    assert res.json()['session_user'] == 'sample_username'

def test_create_session_returns_422_on_empty_username(clean_store):
    body = {
        'session_user': ''
    }

    res = client.post('/sessions/', json=body)
    
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

def test_create_chat_returns_201_when_data_is_valid(setup_store,clean_store):
    request = {
        "role": "user",
        "content": "Hello"
    }

    # Only has initial messages
    assert len(CHAT_STORE[1]) == 2

    res = client.post('/sessions/1/messages/', json=request)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.json() == {"message": "success"}
    
    # appends message to correct chat map
    assert len(CHAT_STORE[1]) == 3

def test_create_chat_returns_404_when_session_does_not_exist(clean_store):
    request = {
        "role": "user",
        "content": "Hello"
    }

    res = client.post('/sessions/1/messages/', json=request)

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_create_chat_returns_422_when_role_is_invalid(clean_store):
    request = {
        "role": "random-role",
        "content": "Hello"
    }

    res = client.post('/sessions/1/messages/', json=request)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_chats_returns_all_chats(setup_store, clean_store):
    expected = [
        {
            "role": "assistant",
            "content": "How may I help you?",
        },
        {
            "role": "user",
            "content": "What is the weather like in London?",
        },
    ]

    res = client.get('/sessions/1/messages/')

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected

def test_get_chats_returns_assistant_chats_as_per_role(setup_store, clean_store):
    expected = [
        {
            "role": "assistant",
            "content": "How may I help you?",
        },
    ]

    res = client.get('/sessions/1/messages/?role=assistant')

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected

def test_get_chats_returns_user_chats_as_per_role(setup_store, clean_store):
    expected = [
        {
            "role": "user",
            "content": "What is the weather like in London?",
        },
    ]

    res = client.get('/sessions/1/messages/?role=user')

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected

def test_get_chats_returns_404_when_session_id_is_invalid(clean_store):
    res = client.get('/sessions/1/messages/')

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_chats_returns_422_when_role_is_invalid(setup_store,clean_store):
    res = client.get('/sessions/1/messages/?role=userX')

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
