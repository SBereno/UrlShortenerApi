import secrets
import string
from sqlalchemy.orm import Session
import model


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def get_db_url_by_key(db: Session, url_key: str) -> model.Url:
    return (
        db.query(model.Url)
        .filter(model.Url.key == url_key)
        .first()
    )


def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while get_db_url_by_key(db, key):
        key = create_random_key()
    return key
