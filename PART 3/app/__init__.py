from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restx import Api
from .config import config
import os
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory function."""
    logger.info("Création de l'application Flask...")
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    # Configuration de l'API
    logger.info("Configuration de l'API...")
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API pour l\'application HBnB',
        doc='/api/v1/',
        prefix='/api/v1'
    )
    
    try:
        logger.info("Importation des endpoints...")
        from .api import auth, users
        
        # Enregistrement des namespaces
        logger.info("Enregistrement des namespaces...")
        api.add_namespace(auth.api)
        api.add_namespace(users.api)
        
        # Log des routes enregistrées
        logger.info("Routes enregistrées:")
        for rule in app.url_map.iter_rules():
            logger.info(f"{rule.endpoint}: {rule.methods} {rule.rule}")
        
        logger.info("Configuration terminée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration: {str(e)}")
        raise
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully!")
    
    return app 