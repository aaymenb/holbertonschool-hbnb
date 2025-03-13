# HBnB - Partie 3 : Authentification et Gestion des Utilisateurs

## Table des matières
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [API Endpoints](#api-endpoints)
5. [Exemples de Code](#exemples-de-code)
6. [FAQ](#faq)

## Introduction

La Partie 3 du projet HBnB implémente un système d'authentification complet. Voici ce que vous pouvez faire :

### Fonctionnalités Principales
1. **Inscription des Utilisateurs**
   - Création de compte avec email et mot de passe
   - Validation des données
   - Stockage sécurisé des mots de passe

2. **Connexion Sécurisée**
   - Authentification avec email/mot de passe
   - Génération de token JWT
   - Protection contre les attaques

3. **Gestion des Utilisateurs**
   - Consultation du profil
   - Modification des informations
   - Suppression de compte

## Installation

### Prérequis
- Python 3.8 ou plus récent
- pip (gestionnaire de paquets Python)
- Git

### Installation Pas à Pas

1. **Créer un environnement virtuel**
```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur Windows :
.\venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate
```

2. **Installer les dépendances**
```bash
# Se placer dans le dossier PART 3
cd "PART 3"

# Installer les packages
pip install -r requirements.txt
```

3. **Configurer l'environnement**
```bash
# Créer le fichier .env
echo "FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre_clé_secrète
DATABASE_URL=sqlite:///hbnb.db" > .env
```

4. **Démarrer l'application**
```bash
python run.py
```

## Configuration

### Structure du Projet
```
PART 3/
├── app/
│   ├── api/              # Routes d'API
│   │   ├── auth.py      # Authentification
│   │   └── users.py     # Gestion utilisateurs
│   ├── models/          # Modèles de données
│   │   ├── base.py     # Classe de base
│   │   └── user.py     # Modèle utilisateur
│   └── repositories/    # Stockage des données
│       ├── base.py     # Interface de base
│       └── user.py     # Repository utilisateur
├── .env                 # Configuration
└── requirements.txt     # Dépendances
```

## API Endpoints

### Routes d'Authentification

1. **Inscription** (`POST /api/v1/auth/register`)
```python
# Exemple de requête
{
    "email": "user@example.com",
    "password": "password123"
}

# Réponse réussie
{
    "message": "Utilisateur créé avec succès",
    "user": {
        "id": 1,
        "email": "user@example.com"
    }
}
```

2. **Connexion** (`POST /api/v1/auth/login`)
```python
# Exemple de requête
{
    "email": "user@example.com",
    "password": "password123"
}

# Réponse réussie
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

3. **Test** (`GET /api/v1/auth/test`)
```python
# Réponse réussie
{
    "message": "API d'authentification fonctionnelle"
}
```

### Routes Utilisateurs

1. **Liste des utilisateurs** (`GET /api/v1/users`)
```python
# Réponse réussie
{
    "users": [
        {
            "id": 1,
            "email": "user@example.com"
        }
    ]
}
```

2. **Détails d'un utilisateur** (`GET /api/v1/users/<id>`)
```python
# Réponse réussie
{
    "user": {
        "id": 1,
        "email": "user@example.com"
    }
}
```

## Exemples de Code

### 1. Création d'un Utilisateur
```python
# Exemple avec requests
import requests

def create_user(email, password):
    url = "http://127.0.0.1:5000/api/v1/auth/register"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la création : {e}")
        return None

# Utilisation
user = create_user("test@example.com", "password123")
if user:
    print(f"Utilisateur créé : {user['user']['email']}")
```

### 2. Connexion et Utilisation du Token
```python
def login_and_get_token(email, password):
    url = "http://127.0.0.1:5000/api/v1/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return None

def get_user_profile(token):
    url = "http://127.0.0.1:5000/api/v1/users/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du profil : {e}")
        return None

# Utilisation
token = login_and_get_token("test@example.com", "password123")
if token:
    profile = get_user_profile(token)
    if profile:
        print(f"Profil utilisateur : {profile}")
```

### 3. Gestion des Erreurs
```python
def handle_auth_error(error):
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 401:
            print("Erreur d'authentification : Token invalide ou expiré")
        elif error.response.status_code == 404:
            print("Erreur : Ressource non trouvée")
        else:
            print(f"Erreur HTTP : {error.response.status_code}")
    else:
        print(f"Erreur : {error}")

# Exemple d'utilisation
try:
    response = requests.get(
        "http://127.0.0.1:5000/api/v1/users/profile",
        headers={"Authorization": "Bearer invalid_token"}
    )
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    handle_auth_error(e)
```

## FAQ

### Questions Fréquentes

**Q: Comment sécuriser mes routes ?**
R: Utilisez le décorateur `@jwt_required()` :
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def protected_route():
    # Récupérer l'ID de l'utilisateur connecté
    current_user_id = get_jwt_identity()
    return {"user_id": current_user_id}
```

**Q: Comment gérer les erreurs d'authentification ?**
R: Utilisez les gestionnaires d'erreurs JWT :
```python
from flask_jwt_extended import JWTManager
from flask import jsonify

jwt = JWTManager()

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "Token invalide",
        "message": "Le token fourni n'est pas valide"
    }), 401

@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        "error": "Token expiré",
        "message": "Le token a expiré, veuillez vous reconnecter"
    }), 401
```

**Q: Comment mettre à jour un utilisateur ?**
R: Utilisez l'endpoint PUT avec le token :
```python
def update_user(token, user_id, new_data):
    url = f"http://127.0.0.1:5000/api/v1/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(url, headers=headers, json=new_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la mise à jour : {e}")
        return None

# Exemple d'utilisation
new_data = {"email": "nouveau@example.com"}
updated_user = update_user(token, 1, new_data)
```

## Support

Pour toute question ou problème :
1. Consultez la documentation Swagger : http://127.0.0.1:5000/api/v1/
2. Vérifiez les logs de l'application
3. Créez une issue sur GitHub

## Bonnes Pratiques

### 1. Sécurité
```python
# Exemple de hachage de mot de passe
from werkzeug.security import generate_password_hash, check_password_hash

# Hachage
password_hash = generate_password_hash("password123")

# Vérification
is_valid = check_password_hash(password_hash, "password123")
```

### 2. Validation des Données
```python
from flask_restx import fields

# Définition du modèle
user_model = api.model('User', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe')
})

# Validation
@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_model)
    def post(self):
        data = api.payload
        # Les données sont automatiquement validées
        return {"message": "Utilisateur créé"}
```

### 3. Gestion des Sessions
```python
# Configuration de la durée de validité du token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Rafraîchissement du token
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    return {"access_token": new_token}
``` 