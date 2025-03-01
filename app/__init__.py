from flask import Flask
from .api.views import api_blueprint  # Importer les routes de l'API

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Charger la configuration

    # Enregistrer le blueprint pour les routes de l'API
    app.register_blueprint(api_blueprint)

    return app
