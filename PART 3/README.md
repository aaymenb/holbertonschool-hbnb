# HBnB - Part 3

Cette partie du projet HBnB implémente l'authentification et l'intégration de la base de données pour le backend.

## Fonctionnalités

- Authentification JWT
- Gestion des utilisateurs avec hachage de mot de passe
- Intégration de base de données SQLite (développement) et MySQL (production)
- Contrôle d'accès basé sur les rôles (admin vs utilisateur)
- API RESTful sécurisée

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
```

2. Activer l'environnement virtuel :
- Windows :
```bash
venv\Scripts\activate
```
- Unix/MacOS :
```bash
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
Créer un fichier `.env` à la racine du projet avec les variables suivantes :
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

5. Initialiser la base de données :
```bash
flask db init
flask db migrate
flask db upgrade
```

## Utilisation

1. Lancer l'application :
```bash
python run.py
```

2. L'API sera accessible à l'adresse : http://127.0.0.1:5000/api/v1/

## Endpoints API

### Authentification
- POST `/api/v1/login` - Connexion utilisateur
- POST `/api/v1/register` - Inscription utilisateur

### Utilisateurs
- GET `/api/v1/users` - Liste des utilisateurs (admin)
- POST `/api/v1/users` - Créer un utilisateur (admin)
- GET `/api/v1/users/<id>` - Obtenir un utilisateur
- PUT `/api/v1/users/<id>` - Mettre à jour un utilisateur
- DELETE `/api/v1/users/<id>` - Supprimer un utilisateur (admin)

## Structure du Projet

```
PART 3/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   ├── models/
│   │   ├── base.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── base.py
│   │   └── user.py
│   ├── services/
│   │   ├── base.py
│   │   └── user.py
│   ├── utils/
│   │   └── auth.py
│   ├── __init__.py
│   └── config.py
├── tests/
├── requirements.txt
└── run.py
```

## Tests

Pour exécuter les tests :
```bash
pytest
```

## Sécurité

- Les mots de passe sont hachés avec bcrypt
- L'authentification utilise JWT
- Les endpoints sensibles sont protégés par des décorateurs
- Les rôles utilisateur sont gérés (admin vs utilisateur normal)

## Base de Données

- Développement : SQLite
- Production : MySQL

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request 