from .base import BaseModel

class Amenity(BaseModel):
    """Modèle pour les commodités"""
    
    def __init__(self, name):
        """Initialise une nouvelle commodité"""
        super().__init__()
        self.name = name
        self.places = []
    
    def to_dict(self):
        """Convertit la commodité en dictionnaire"""
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name
        })
        return base_dict 