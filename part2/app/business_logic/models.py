from datetime import datetime
import uuid

class BaseModel:
    """Base model with common attributes and methods."""
    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class User(BaseModel):
    """User class representing a system user."""
    def __init__(self, email, password, first_name="", last_name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Place(BaseModel):
    """Place class representing a listing."""
    def __init__(self, name, description, city_id, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.city_id = city_id
        self.user_id = user_id
        self.amenities = []  # Many-to-many relationship with Amenity

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

class Review(BaseModel):
    """Review class representing a user review on a place."""
    def __init__(self, user_id, place_id, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.place_id = place_id
        self.text = text

class Amenity(BaseModel):
    """Amenity class representing services available in a place."""
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
