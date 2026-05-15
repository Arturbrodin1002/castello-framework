from sqlalchemy.orm import Session

from src.main.api.db.models.user_table import User
from src.main.api.models.create_user_request import CreateUserRequest


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()


    @staticmethod
    def create_user(db: Session, create_user_request: CreateUserRequest) -> User:
        user = User(
            username=create_user_request.username,
            password=create_user_request.password,
            role=create_user_request.role,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
