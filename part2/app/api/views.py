from flask import Blueprint, request, jsonify
from app.persistence.facade import Facade
from app.persistence.in_memory_repository import InMemoryRepository
from app.business_logic.user_logic import UserLogic

# Initialiser les composants
repository = InMemoryRepository()
user_logic = UserLogic(repository)
facade = Facade(repository, user_logic)

# Créer un Blueprint pour l'API
api_blueprint = Blueprint('api', __name__)

# Route pour créer un utilisateur
@api_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtenir les données JSON envoyées
    try:
        user = facade.create_user(data)
        return jsonify({"id": user.id, "name": user.name}), 201  # Retourner l'utilisateur créé
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Erreur si les données sont invalides

# Route pour récupérer un utilisateur par son ID
@api_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = facade.get_user(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name})  # Retourner l'utilisateur
    else:
        return jsonify({"error": "User not found"}), 404  # Utilisateur non trouvé

