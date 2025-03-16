# HBnB - Part 2

Ce projet est la deuxième partie de l'application HBnB (Holberton BnB), une plateforme de location de logements.

## Structure du Projet

```
api/
├── __init__.py
├── v1/
│   ├── __init__.py
│   ├── endpoints/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   └── amenity.py
├── repositories/
│   ├── __init__.py
│   └── in_memory_repository.py
└── services/
    ├── __init__.py
    └── facade.py
```

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

## Utilisation

Pour lancer l'application :
```bash
python -m flask run
```


## Documentation API

La documentation Swagger de l'API est disponible à l'adresse : http://localhost:5000/api/v1/ 