from typing import Optional
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""
    
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return User.query.filter_by(email=email).first()

    def create(self, obj_in: dict) -> User:
        """Create a new user with password hashing."""
        if 'password' in obj_in:
            password = obj_in.pop('password')
            user = super().create(obj_in)
            user.password = password
            return user
        return super().create(obj_in)

    def update(self, db_obj: User, obj_in: dict) -> User:
        """Update user with password hashing if provided."""
        if 'password' in obj_in:
            password = obj_in.pop('password')
            user = super().update(db_obj, obj_in)
            user.password = password
            return user
        return super().update(db_obj, obj_in) 