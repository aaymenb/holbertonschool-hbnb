from datetime import datetime
import uuid

class BaseModel:
    """Classe de base pour tous les modèles"""
    
    def __init__(self):
        """Initialise un nouveau modèle"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, **kwargs):
        """Met à jour les attributs de l'objet"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow() 