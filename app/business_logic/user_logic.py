class UserLogic:
    def __init__(self, repository):
        self.repository = repository  # Utiliser le repository pour stocker les utilisateurs

    def create_user(self, data):
        if not data.get('name'):  # Vérifier si le nom de l'utilisateur est présent
            raise ValueError("User must have a name.")
        
        # Créer un objet User et lui attribuer un ID
        user = User(id=len(self.repository.storage) + 1, name=data['name'])
        return user

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
