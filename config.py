class Config:
    SECRET_KEY = 'maclésecrete3009'
    FLASK_ENV = 'development'        # Environnement de développement
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Base de données SQLite (pour la partie 3)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications non suivies

