from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, email, password, first_name='', last_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

