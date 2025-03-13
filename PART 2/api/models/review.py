from .base import BaseModel

class Review(BaseModel):
    """Modèle pour les avis"""
    
    def __init__(self, user_id, place_id, text):
        """Initialise un nouvel avis"""
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = text
    
    def to_dict(self):
        """Convertit l'avis en dictionnaire"""
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'place_id': self.place_id,
            'text': self.text
        })
        return base_dict 