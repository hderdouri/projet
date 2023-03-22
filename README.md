# **FastAPI Authentification**

Ceci est un exemple de projet FastAPI pour une API RESTful de base, qui permet l'authentification avec JWT.

* Installation
Clonez le dépôt
cd dans le dossier du projet
Installez les dépendances: pip install -r requirements.txt
Créez une base de données en exécutant python db.py
Lancez l'application avec uvicorn main:app --reload

* Utilisation
L'application expose plusieurs endpoints pour interagir avec une liste d'éléments.

* Créer un utilisateur
Créez un utilisateur en effectuant une requête POST vers /signup avec les paramètres username et password.


* Authentifier un utilisateur
Authentifiez un utilisateur en effectuant une requête POST vers /signin avec les paramètres username et password.




* Récupérer un élément
Récupérez un élément en effectuant une requête GET vers /items/{item_id}, où {item_id} est l'ID de l'élément.





