# Installer pymongo

`pip install pymongo`

# Lancer le démon

`sudo /etc/init.d/mongodb start`

# Importer

`import pymongo`

# Ouverture du client

`client = pymongo.MongoClient('mongodb://localhost:27017')`

# Ouverture de la bdd

`db = client['pymongo_test']`

# Insertion de données

```python
posts = db.posts
post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))
```

```python
empreintes = db.empreintes
empreinte = {
	'x': x,
	'y': y,
	'balise1': 20,
	'balise2': 20,
	'balise3': 20,
	...
}
result = empreintes.insert_one(empreinte)
print('Une empreinte: {}' % result.inserted_id)
```

# Récupération des données

```python
bills_post = posts.find_one({'author': 'Bill'})
print(bills_post)

empreinte = empreintes.find({
	'balise1': truc,
})
```

```python
empreintes = posts.find_one({'x': x, 'y': y})
print(empreintes)

empreinte = empreintes.find({
	'x': x,
	'y': y
})
```
