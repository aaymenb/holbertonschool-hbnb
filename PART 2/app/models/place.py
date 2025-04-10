from .base import BaseModel

class Place(BaseModel):
    """Modèle pour les lieux"""
    
    def __init__(self, owner_id, name, description, number_rooms, number_bathrooms,
                 max_guest, price_by_night, latitude, longitude):
        """Initialise un nouveau lieu"""
        super().__init__()
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guest = max_guest
        self.price_by_night = price_by_night
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []
        self.reviews = []
    
    def to_dict(self):
        """Convertit le lieu en dictionnaire"""
        base_dict = super().to_dict()
        base_dict.update({
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'number_rooms': self.number_rooms,
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'price_by_night': self.price_by_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews': [review.to_dict() for review in self.reviews]
        })
        return base_dict 