# README

Ce dépôt contient plusieurs scripts Python permettant de géolocaliser un module XBee sur un plan.

Les scripts suivants sont exécutables :
- `app.py` lance un serveur qui permet d'afficher la position d'un objet sur un plan, de mettre à jour sa position ou de retourner sa position au format JSON
- `fingerprinting.py` permet d'effectuer la cartographie radio d'une pièce
- `geoloc.py` permet d'effectuer la géolocalisation proprement dit à partir des données récoltées lors de la phase de fingerprinting

Ils se basent sur les scripts suivants :
- `at.py` permet de communiquer en mode AT avec d'autres modules XBee jouant le rôle de balises
- `db.py` permet d'effectuer des opérations sur une base de données MongoDB
- `matrix.py` qui sert de structure de données permettant de comparer les empreintes RSSI stockées et de déterminer les plus similaires à une empreinte donnée
