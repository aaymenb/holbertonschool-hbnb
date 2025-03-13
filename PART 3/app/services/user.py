from typing import Optional
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.base import BaseService

class UserService(BaseService[User]):
    """Service for User business logic."""
    
    def __init__(self):
        repository = UserRepository()
        super().__init__(repository)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.repository.get_by_email(email)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = self.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    def create(self, obj_in: dict) -> User:
        """Create a new user."""
        if self.get_by_email(obj_in['email']):
            raise ValueError("Email already registered")
        return super().create(obj_in)

    def update(self, id: str, obj_in: dict) -> Optional[User]:
        """Update a user."""
        if 'email' in obj_in:
            existing_user = self.get_by_email(obj_in['email'])
            if existing_user and existing_user.id != id:
                raise ValueError("Email already registered")
        return super().update(id, obj_in) 