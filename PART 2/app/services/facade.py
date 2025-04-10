from typing import List, Optional, Type, TypeVar, Generic
from ..models.base import BaseModel
from ..repositories.in_memory_repository import InMemoryRepository

T = TypeVar('T', bound=BaseModel)

class Facade(Generic[T]):
    """Facade pour gérer la communication entre les couches"""
    
    def __init__(self, model_class: Type[T]):
        """Initialise le facade"""
        self.repository = InMemoryRepository(model_class)
    
    def create(self, **kwargs) -> T:
        """Crée un nouvel objet"""
        return self.repository.create(**kwargs)
    
    def get(self, id: str) -> Optional[T]:
        """Récupère un objet par son ID"""
        return self.repository.get(id)
    
    def get_all(self) -> List[T]:
        """Récupère tous les objets"""
        return self.repository.get_all()
    
    def update(self, id: str, **kwargs) -> Optional[T]:
        """Met à jour un objet"""
        return self.repository.update(id, **kwargs)
    
    def delete(self, id: str) -> bool:
        """Supprime un objet"""
        return self.repository.delete(id) 