from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token
from app.services.user import UserService
import logging

logger = logging.getLogger(__name__)

api = Namespace('auth', description='Authentication operations', path='/auth')
user_service = UserService()

# Modèles pour la documentation Swagger
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name')
})

@api.route('/')
class AuthRoot(Resource):
    def get(self):
        """Root route for auth namespace."""
        logger.info("Auth root route accessed")
        return jsonify({"message": "Auth namespace is working!"})

@api.route('/test')
class Test(Resource):
    def get(self):
        """Test route to verify API is working."""
        logger.info("Route /test accessed")
        logger.info(f"Current app: {current_app}")
        logger.info(f"Current app routes: {list(current_app.url_map.iter_rules())}")
        return jsonify({"message": "Auth API is working!"})

@api.route('/ping')
class Ping(Resource):
    def get(self):
        """Simple ping route to test API connectivity."""
        logger.info("Route /ping accessed")
        return jsonify({"status": "ok", "message": "pong"})

@api.route('/login')
class Login(Resource):
    @api.expect(user_model)
    def post(self):
        """Login user and return JWT token."""
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            if 'email' not in data or 'password' not in data:
                return {"error": "Missing email or password"}, 400

            user = user_service.authenticate(data['email'], data['password'])
            if not user:
                return {"error": "Invalid email or password"}, 401

            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "user": user.to_dict()
            }
        except Exception as e:
            return {"error": str(e)}, 500

@api.route('/register')
class Register(Resource):
    @api.expect(user_model)
    def post(self):
        """Register a new user."""
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            if 'email' not in data or 'password' not in data:
                return {"error": "Missing email or password"}, 400

            user = user_service.create(data)
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "user": user.to_dict()
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500 