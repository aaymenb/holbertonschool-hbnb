sequenceDiagram
%% Inscription d'un utilisateur
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Envoi des informations d'inscription
API->>BusinessLogic: Valider les informations
BusinessLogic->>Database: Vérifier si l'utilisateur existe déjà
Database-->>BusinessLogic: Réponse de vérification
BusinessLogic->>Database: Sauvegarder les informations de l'utilisateur
Database-->>BusinessLogic: Confirmation de la sauvegarde
BusinessLogic-->>API: Retourner la réponse (succès/échec)
API-->>User: Réponse d'inscription réussie ou échec


%% Création d'un lieu
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Envoi des informations sur le lieu
API->>BusinessLogic: Valider les informations du lieu
BusinessLogic->>Database: Vérifier les données (disponibilité, etc.)
Database-->>BusinessLogic: Réponse de validation
BusinessLogic->>Database: Sauvegarder le lieu
Database-->>BusinessLogic: Confirmation de la sauvegarde
BusinessLogic-->>API: Retourner la réponse (succès/échec)
API-->>User: Réponse de création de lieu réussie ou échec


%% Soumission d'un avis
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Soumettre un avis pour un lieu
API->>BusinessLogic: Valider le contenu de l'avis
BusinessLogic->>Database: Vérifier l'existence du lieu
Database-->>BusinessLogic: Réponse de vérification
BusinessLogic->>Database: Sauvegarder l'avis
Database-->>BusinessLogic: Confirmation de la sauvegarde
BusinessLogic-->>API: Retourner la réponse (succès/échec)
API-->>User: Confirmation de soumission de l'avis


%% Récupération de la liste des lieux
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Demande de la liste des lieux (avec critères)
API->>BusinessLogic: Traiter les critères de recherche
BusinessLogic->>Database: Requête pour récupérer les lieux
Database-->>BusinessLogic: Retourner les résultats
BusinessLogic-->>API: Retourner les données des lieux
API-->>User: Afficher la liste des lieux

