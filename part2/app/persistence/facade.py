class Facade:
    def __init__(self, repository, user_logic):
        self.repository = repository
        self.user_logic = user_logic

    def create_user(self, data):
        user = self.user_logic.create_user(data)
        self.repository.add(user)
        return user

    def get_user(self, user_id):
        return self.repository.get(user_id)
