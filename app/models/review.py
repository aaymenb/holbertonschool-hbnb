from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user, place, text, rating, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.place = place
        self.text = text
        self.rating = rating

    def __str__(self):
        return f"Review for {self.place.name} by {self.user.first_name} {self.user.last_name}"
