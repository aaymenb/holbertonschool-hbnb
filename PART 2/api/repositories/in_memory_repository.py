from typing import Dict, List, Optional, Type, TypeVar, Generic
from ..models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class InMemoryRepository(Generic[T]):
    """Repository en mémoire pour stocker les objets"""
    
    def __init__(self, model_class: Type[T]):
        """Initialise le repository"""
        self.model_class = model_class
        self._storage: Dict[str, T] = {}
    
    def create(self, **kwargs) -> T:
        """Crée un nouvel objet"""
        obj = self.model_class(**kwargs)
        self._storage[obj.id] = obj
        return obj
    
    def get(self, id: str) -> Optional[T]:
        """Récupère un objet par son ID"""
        return self._storage.get(id)
    
    def get_all(self) -> List[T]:
        """Récupère tous les objets"""
        return list(self._storage.values())
    
    def update(self, id: str, **kwargs) -> Optional[T]:
        """Met à jour un objet"""
        obj = self.get(id)
        if obj:
            obj.update(**kwargs)
        return obj
    
    def delete(self, id: str) -> bool:
        """Supprime un objet"""
        if id in self._storage:
            del self._storage[id]
            return True
        return False 