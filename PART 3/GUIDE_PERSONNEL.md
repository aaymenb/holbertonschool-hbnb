# Guide Personnel - PART 3 HBnB

## 1. Comprendre l'Architecture

### 1.1 Structure des Dossiers
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
```

### 1.2 Rôle de Chaque Composant

#### Models (Modèles)
- `base.py` : Classe de base pour tous les modèles
  ```python
  class Base:
      def __init__(self):
          self.id = None
          self.created_at = None
          self.updated_at = None
  ```

- `user.py` : Modèle utilisateur
  ```python
  class User(Base):
      def __init__(self):
          super().__init__()
          self.email = None
          self.password = None
  ```

#### Repositories (Stockage)
- `base.py` : Interface de base pour le stockage
  ```python
  class BaseRepository:
      def create(self, obj):
          pass
      
      def get(self, id):
          pass
      
      def update(self, obj):
          pass
      
      def delete(self, id):
          pass
  ```

- `user.py` : Gestion du stockage des utilisateurs
  ```python
  class UserRepository(BaseRepository):
      def __init__(self):
          self.users = {}  # Stockage en mémoire
      
      def create(self, user):
          user.id = len(self.users) + 1
          self.users[user.id] = user
          return user
  ```

#### API (Routes)
- `auth.py` : Routes d'authentification
  ```python
  @api.route('/register')
  class Register(Resource):
      def post(self):
          # Création d'un utilisateur
          pass
      
  @api.route('/login')
  class Login(Resource):
      def post(self):
          # Connexion et génération de token
          pass
  ```

## 2. Fonctionnement de l'Authentification

### 2.1 Processus d'Inscription
1. L'utilisateur envoie email et mot de passe
2. Le système vérifie que l'email n'existe pas
3. Le mot de passe est haché
4. Un nouvel utilisateur est créé
5. Une réponse de succès est renvoyée

```python
# Exemple de code
@api.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Vérification
        if not email or not password:
            return {"error": "Email et mot de passe requis"}, 400
            
        # Création
        user = User()
        user.email = email
        user.password = generate_password_hash(password)
        
        # Sauvegarde
        user = user_repository.create(user)
        
        return {"message": "Utilisateur créé", "user": user.to_dict()}
```

### 2.2 Processus de Connexion
1. L'utilisateur envoie email et mot de passe
2. Le système vérifie les identifiants
3. Un token JWT est généré
4. Le token est renvoyé à l'utilisateur

```python
# Exemple de code
@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Vérification
        user = user_repository.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return {"error": "Identifiants invalides"}, 401
            
        # Génération du token
        token = create_access_token(identity=user.id)
        
        return {"access_token": token}
```

## 3. Protection des Routes

### 3.1 Utilisation du Token
```python
# Exemple de route protégée
@jwt_required()
def protected_route():
    current_user_id = get_jwt_identity()
    return {"user_id": current_user_id}
```

### 3.2 Gestion des Erreurs
```python
# Gestion des tokens invalides
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "Token invalide",
        "message": "Le token fourni n'est pas valide"
    }), 401

# Gestion des tokens expirés
@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        "error": "Token expiré",
        "message": "Le token a expiré, veuillez vous reconnecter"
    }), 401
```

## 4. Exemples d'Utilisation

### 4.1 Création d'un Utilisateur
```python
import requests

def create_user(email, password):
    url = "http://127.0.0.1:5000/api/v1/auth/register"
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Utilisation
user = create_user("test@example.com", "password123")
print(user)
```

### 4.2 Connexion et Accès aux Routes Protégées
```python
def login_and_access_protected():
    # 1. Connexion
    login_url = "http://127.0.0.1:5000/api/v1/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(login_url, json=login_data)
    token = response.json()['access_token']
    
    # 2. Accès à une route protégée
    protected_url = "http://127.0.0.1:5000/api/v1/users/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(protected_url, headers=headers)
    return response.json()
```

## 5. Points Importants à Retenir

### 5.1 Sécurité
- Les mots de passe sont toujours hachés avant stockage
- Les tokens JWT sont utilisés pour l'authentification
- Les routes sensibles sont protégées
- Les erreurs sont gérées proprement

### 5.2 Bonnes Pratiques
- Validation des données d'entrée
- Gestion des erreurs appropriée
- Messages d'erreur clairs
- Code modulaire et réutilisable

### 5.3 Points d'Attention
- Ne jamais stocker les mots de passe en clair
- Toujours vérifier les tokens
- Gérer les erreurs d'authentification
- Limiter les tentatives de connexion

## 6. Questions Fréquentes et Réponses

### 6.1 Questions sur l'Authentification
Q: Comment fonctionne le système de tokens ?
R: Le système utilise JWT (JSON Web Tokens) :
1. À la connexion, un token est généré
2. Le token contient l'ID de l'utilisateur
3. Le token est envoyé dans l'en-tête Authorization
4. Le serveur vérifie le token à chaque requête

### 6.2 Questions sur la Sécurité
Q: Comment sont protégés les mots de passe ?
R: Les mots de passe sont hachés avec Werkzeug :
```python
# Hachage
password_hash = generate_password_hash(password)

# Vérification
is_valid = check_password_hash(password_hash, password)
```

### 6.3 Questions sur les Routes
Q: Comment protéger une route ?
R: Utilisez le décorateur `@jwt_required()` :
```python
@jwt_required()
def protected_route():
    current_user_id = get_jwt_identity()
    return {"user_id": current_user_id}
```

## 7. Conseils pour le Développement

### 7.1 Ajout de Nouvelles Fonctionnalités
1. Créer le modèle si nécessaire
2. Ajouter le repository
3. Créer les routes d'API
4. Ajouter la documentation
5. Tester la fonctionnalité

### 7.2 Débogage
1. Vérifier les logs
2. Tester les endpoints
3. Vérifier les tokens
4. Valider les données

### 7.3 Tests
1. Tester l'inscription
2. Tester la connexion
3. Tester les routes protégées
4. Tester la gestion des erreurs 