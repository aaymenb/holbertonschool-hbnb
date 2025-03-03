class InMemoryRepository:
    def __init__(self):
        self.storage = {}  # Dictionnaire pour stocker les utilisateurs en mémoire

    def add(self, user):
        self.storage[user.id] = user

    def get(self, user_id):
        return self.storage.get(user_id)
