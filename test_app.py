import requests
import os

url = 'http://127.0.0.1:5000/'
cv_path = r'c:\Users\ayman\Desktop\CV_adapter\dummy_cv.tex'
job_description = """Descriptif du poste
En tant qu'Ingénieure/Ingénieur DevOps au sein de notre équipe, vous aurez l'opportunité d'approfondir vos connaissances dans le domaine des architectures middleware et de l'intégration continue.

A la DSI de la Banque Postale et Assurance (1800 collaborateurs à Nantes, Toulouse, Issy Les Moulineaux et Gradignan), vos actions auront un impact positif sur nos clients pour une finance plus responsable et une transition juste.

Vos missions

La plateforme d'échanges EAI de la salle des marchés interconnecte les différentes applications de la DSIBAet facilite les échanges avec l'extérieur.

Dans le cadre du projet EAI de la Direction des Marchés de La Banque Postale, nous recherchons un(e) stagiaire pour intervenir sur plusieurs chantiers stratégiques, dont les objectifs principaux sont :

Optimiser la chaîne d'intégration continue
Assurer le maintien en condition opérationnelle
Préparer une migration majeure du socle technique
Encadré par un ingénieur confirmé, les missions proposées sont les suivantes :

Mettre en place des tests de non-régression (TNR) : Utilisation d'un outil interne pour orchestrer et automatiser les TNR pour environ 300 flux Tibco.
Améliorer les pipelines Jenkins existants : Refactorisation, intégration des bonnes pratiques CI/CD.
Participer aux travaux d'inventaire des flux Tibco : Structuration et documentation des flux déployés et des TNR pour faciliter leur suivi, leur gouvernance et leur maintien.
Environnement technique :

Intégration continue : Jenkins, Maven, Groovy, Bash
Socle technique : Tibco BusinessWorks 5.x, Apache Camel, Java, PHP
Gestion des sources et livrables : Git, JFrog Artifactory
Environnement de développement Windows, Serveurs applicatifs Linux
VOTRE EQUIPE

Vous serez intégré au sein des équipes pré-trade du Domaine Marché (MAR/PRE) du Centre de solution de la BEDL et PRO (Banque des entreprises et du développement local et banque des pro).

L'équipe IT Marché est composée d'environ 40 collaborateurs. Elle a la charge du support et du développement des applications de la salle des marchés, couvrant différentes équipes et fonctions métiers (trader, vendeur, Middle et Back Office, Risque). L'équipe EAI que vous rejoindrez est composée de 3 collaborateurs."""
email = 'aymanemerbouh03@gmail.com'

files = {'cv_file': open(cv_path, 'rb')}
data = {'job_description': job_description, 'email': email}

try:
    print(f"Sending request to {url}...")
    print(f"Email: {email}")
    print(f"CV: {cv_path}")
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        print("Success! PDF received.")
        with open('test_output_user.pdf', 'wb') as f:
            f.write(response.content)
        print("Saved response to test_output_user.pdf")
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
