from sqlalchemy.orm import Session
from models.user import User

def select_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()