from flask_restx import Namespace, Resource, fields
from ...models.user import User
from ...services.facade import Facade

api = Namespace('users', description='Opérations liées aux utilisateurs')

# Schémas pour la documentation Swagger
user_schema = api.model('User', {
    'id': fields.String(readonly=True, description='Identifiant unique de l\'utilisateur'),
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur'),
    'created_at': fields.DateTime(readonly=True, description='Date de création'),
    'updated_at': fields.DateTime(readonly=True, description='Date de dernière mise à jour')
})

user_input = api.model('UserInput', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur')
})

# Service Facade pour les utilisateurs
user_facade = Facade(User)

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_schema)
    def get(self):
        """Liste tous les utilisateurs"""
        return user_facade.get_all()
    
    @api.doc('create_user')
    @api.expect(user_input)
    @api.marshal_with(user_schema, code=201)
    def post(self):
        """Crée un nouvel utilisateur"""
        user = user_facade.create(**api.payload)
        return user, 201

@api.route('/<string:id>')
@api.param('id', 'Identifiant de l\'utilisateur')
class UserItem(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_schema)
    def get(self, id):
        """Récupère un utilisateur par son ID"""
        user = user_facade.get(id)
        if user is None:
            api.abort(404, f"L'utilisateur {id} n'existe pas")
        return user
    
    @api.doc('update_user')
    @api.expect(user_input)
    @api.marshal_with(user_schema)
    def put(self, id):
        """Met à jour un utilisateur"""
        user = user_facade.get(id)
        if user is None:
            api.abort(404, f"L'utilisateur {id} n'existe pas")
        updated_user = user_facade.update(id, **api.payload)
        return updated_user 