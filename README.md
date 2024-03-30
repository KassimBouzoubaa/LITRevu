# Application de Critiques de Livres et d'Articles

## Introduction
Cette application offre une plateforme pour demander, lire et publier des critiques de livres ou d'articles. Elle est développée avec Django et utilise une base de données SQLite.

## Fonctionnalités

### Utilisateurs

- **Inscription et Connexion** : Les utilisateurs peuvent s'inscrire et se connecter pour accéder aux fonctionnalités de l'application.

- **Gestion des Utilisateurs** : Les utilisateurs peuvent consulter, suivre et arrêter de suivre d'autres utilisateurs.

### Billets et Critiques

- **Création de Billets** : Les utilisateurs peuvent créer des billets pour demander des critiques sur des livres ou des articles.

- **Réponses aux Billets** : Les utilisateurs peuvent répondre aux billets en postant des critiques.

### Authentification

- **Pages d'Authentification** : Des pages d'inscription et de connexion sont fournies pour les utilisateurs.

### Développeurs

- **Environnement Local** : Les développeurs peuvent créer un environnement local en suivant la documentation fournie.

## Spécifications Techniques

- **Framework** : Django
- **Base de Données** : SQLite (fichier db.sqlite3 inclus dans le repository)
## Installation
Pour utiliser ce logiciel, veuillez suivre ces étapes d'installation :

1. Clonez le référentiel depuis GitHub :

```bash
git clone https://github.com/KassimBouzoubaa/LITRevu.git
```
2. Accédez au répertoire du projet :
```bash
cd Développez_une_application_Web_en_utilisant_Django
```
3. Créez un environnement virtuel Python pour isoler les dépendances :
```bash
python -m venv env
```
4. Activez l'environnement virtuel :
```bash
source venv/bin/activate
```
5. Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

6. Appliquer les migrations :
```bash
python manage.py migrate
```

7. Lancer le serveur : :
```bash
python manage.py runserver
```


## Utilisation

1. Accéder à l'application via votre navigateur web à l'adresse : `http://localhost:8000/`

2. S'inscrire ou se connecter pour accéder aux fonctionnalités de l'application.

3. Explorer les billets, les critiques et interagir avec d'autres utilisateurs.


## Auteur

BOUZOUBAA Kassim


