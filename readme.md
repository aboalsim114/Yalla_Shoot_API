# YallaShoot Backend

![YallaShoot](https://i.ibb.co/Gx4CdMP/DALL-E-2024-03-29-20-48-11-Design-a-favicon-logo-for-a-web-application-named-Yalla-Shoot-The-logo-sh.webp)

YallaShoot Backend est une API conçue pour gérer les matchs de football, permettant aux utilisateurs de s'inscrire, de créer et de gérer des équipes, de planifier des matchs, de s'inscrire à des matchs existants, et de suivre leurs activités sportives. Cette API offre également une fonctionnalité de messagerie pour permettre aux utilisateurs de communiquer entre eux.

## Caractéristiques

- Gestion des utilisateurs et authentification JWT.
- Création et gestion des équipes.
- Planification et inscription aux matchs.
- Suivi des activités sportives des joueurs.
- Système de messagerie interne.
- Notifications pour les demandes de participation et les mises à jour de statut.

## Technologies Utilisées

- Django et Django Rest Framework pour la création de l'API.
- SQLite pour la base de données en développement
- Simple JWT pour l'authentification via Token.
- DRF-YASG pour la génération de la documentation Swagger.

## Installation

Pour exécuter ce projet localement, suivez ces étapes :

1. Clonez le dépôt :

```bash 
https://github.com/aboalsim114/Yalla_Shoot_API.git
```

2. Accédez au dossier du projet :

```bash
cd Yalla_Shoot_API
```


3. Installez les dépendances en utilisant `pip` :

```bash 
pip install -r requirements.txt
```
4. Effectuez les migrations de la base de données :
```bash
python manage.py makemigrations
python manage.py migrate
```


5. Lancez le serveur de développement :
```bash
python manage.py runserver
```


Une fois le serveur lancé, accédez à `http://127.0.0.1:8000/swagger/` pour voir la documentation Swagger de l'API, vous permettant de tester facilement tous les endpoints disponibles.


