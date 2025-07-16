'''
    Keeps hold of active sessions
'''
SESSION_STORE = []


'''
    Keeps hold of chats mapped to the active sessions
    Key -> session id
    Val -> list<chats>
'''
CHAT_STORE = {}