from flask import Flask, jsonify
from flask_restx import Api
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

def create_app():
    """Crée et configure l'application Flask"""
    logger.info("Création de l'application Flask...")
    app = Flask(__name__)
    
    # Configuration de l'API
    logger.info("Configuration de l'API...")
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API pour l\'application HBnB',
        doc='/api/v1/'
    )
    
    # Route de base
    @app.route('/')
    def index():
        logger.info("Accès à la route principale")
        return jsonify({
            'message': 'Bienvenue sur l\'API HBnB',
            'version': '1.0',
            'endpoints': {
                'users': '/api/v1/users',
                'places': '/api/v1/places',
                'reviews': '/api/v1/reviews',
                'amenities': '/api/v1/amenities'
            }
        })
    
    try:
        logger.info("Importation des endpoints...")
        from .v1.endpoints import users, places, reviews, amenities
        
        # Enregistrement des namespaces
        logger.info("Enregistrement des namespaces...")
        api.add_namespace(users.api, path='/api/v1/users')
        api.add_namespace(places.api, path='/api/v1/places')
        api.add_namespace(reviews.api, path='/api/v1/reviews')
        api.add_namespace(amenities.api, path='/api/v1/amenities')
        
        logger.info("Configuration terminée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration: {str(e)}")
        raise
    
    return app 