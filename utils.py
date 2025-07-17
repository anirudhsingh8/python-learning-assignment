from datetime import datetime, timezone

"""Cleans a username by stripping whitespace and converting to lowercase."""
def clean_username(username: str):
    return username.strip().lower()

"""Returns the current UTC timestamp in ISO format."""
def get_current_utc_timestamp():
    return datetime.now(timezone.utc).isoformat()