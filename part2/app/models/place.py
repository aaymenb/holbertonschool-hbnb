from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, city, name, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = city
        self.name = name
        self.description = description
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
