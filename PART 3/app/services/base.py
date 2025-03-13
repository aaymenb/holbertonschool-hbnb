from typing import TypeVar, Generic, Type, Optional, List, Any, Dict, Union
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")

class BaseService(Generic[ModelType]):
    """Base service class for business logic."""
    
    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    def get(self, id: str) -> Optional[ModelType]:
        """Get a single record by id."""
        return self.repository.get(id)

    def get_all(self) -> List[ModelType]:
        """Get all records."""
        return self.repository.get_all()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        return self.repository.create(obj_in)

    def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Update a record."""
        db_obj = self.get(id)
        if db_obj:
            return self.repository.update(db_obj, obj_in)
        return None

    def delete(self, id: str) -> bool:
        """Delete a record."""
        return self.repository.delete(id)

    def exists(self, **kwargs) -> bool:
        """Check if a record exists."""
        return self.repository.exists(**kwargs) 