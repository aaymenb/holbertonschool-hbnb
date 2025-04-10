from .base import BaseModel

class User(BaseModel):
    """Modèle pour les utilisateurs"""
    
    def __init__(self, email, password, first_name=None, last_name=None):
        """Initialise un nouvel utilisateur"""
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
    
    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire"""
        base_dict = super().to_dict()
        base_dict.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        })
        return base_dict 