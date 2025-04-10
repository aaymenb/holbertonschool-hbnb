from app import db
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict, Union
from uuid import uuid4

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """Base repository class for database operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, id: str) -> Optional[ModelType]:
        """Get a single record by id."""
        return self.model.query.get(id)

    def get_all(self) -> List[ModelType]:
        """Get all records."""
        return self.model.query.all()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        obj_in['id'] = str(uuid4())
        db_obj = self.model(**obj_in)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update a record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def delete(self, id: str) -> bool:
        """Delete a record."""
        obj = self.get(id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def exists(self, **kwargs) -> bool:
        """Check if a record exists."""
        return self.model.query.filter_by(**kwargs).first() is not None 