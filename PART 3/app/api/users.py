from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user import UserService
from app.utils.auth import admin_required, get_current_user

api = Namespace('users', description='User operations')
user_service = UserService()

# Modèles pour la documentation Swagger
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='User admin status')
})

@api.route('')
class UserList(Resource):
    @api.doc('list_users', security='apikey')
    @api.marshal_list_with(user_model)
    @jwt_required()
    @admin_required()
    def get(self):
        """List all users (admin only)."""
        users = user_service.get_all()
        return [user.to_dict() for user in users]

    @api.doc('create_user', security='apikey')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    @admin_required()
    def post(self):
        """Create a new user (admin only)."""
        data = request.get_json()
        try:
            user = user_service.create(data)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<id>')
@api.param('id', 'The user identifier')
class User(Resource):
    @api.doc('get_user', security='apikey')
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, id):
        """Get a specific user."""
        user = user_service.get(id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.doc('update_user', security='apikey')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, id):
        """Update a user."""
        current_user = get_current_user()
        if not current_user.is_admin and current_user.id != id:
            api.abort(403, "Not authorized")
        
        data = request.get_json()
        try:
            user = user_service.update(id, data)
            if not user:
                api.abort(404, "User not found")
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_user', security='apikey')
    @jwt_required()
    @admin_required()
    def delete(self, id):
        """Delete a user (admin only)."""
        if user_service.delete(id):
            return '', 204
        api.abort(404, "User not found") 