class SessionModel:
    session_id: int
    session_user: str
    created_at: str

    def __init__(self, session_id, session_user, created_at):
        self.session_id = session_id
        self.session_user = session_user
        self.created_at = created_at