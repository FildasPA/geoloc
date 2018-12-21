# Snippets Pymongo

## Installer Pymongo

`pip install pymongo`

## Lancer le démon mongodb

`sudo /etc/init.d/mongodb start`

## Implémentation

```python
import pymongo

# Initialisation du client Mongodb
client = pymongo.MongoClient('mongodb://localhost:27017')
# Accès à la base de données
db = self.client.get_database('db_name')
```

## Opérations sur une collection (= table)

```python
# Récupérer le contenu de la collection
db.fingers.find()
# Ou
db.getCollection('fingers').find()

# Insérer des données
db.fingers.insert_one({'x': 3})

# Vider la collection
db.fingers.remove()
```
