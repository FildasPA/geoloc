#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""La classe DB définie dans ce script permet d'effectuer des opérations sur une
base de données de type MongoDB (NoSQL). Elle permet entre autres :
- d'initialiser la connexion
- d'insérer une nouvelle entrée
- retourner toutes les entrées présentes dans la base
- supprimer toutes les entrées"""

import pymongo

import term

# Adresse de la base
URI = 'mongodb://localhost:27017'
# Nom de la bdd
DB_NAME = 'cartographie1'


class DB:
    def __init__(self):
        """Initialise la connexion avec la BDD"""
        self.client = pymongo.MongoClient(URI)
        self.db = self.client.get_database(DB_NAME)


    def __del__(self):
        # self.db.close() # Si besoin de fermer la connexion manuellement
        pass

    def insert(self, values):
        """Insère une nouvelle entrée dans la base.
        values = {'x': N, 'y': N, 'BALISE_1': N, 'BALISE_2': N, ..., 'BALISE_5': N}"""
        self.db.fingers.insert_one(values)
        print("%s: %s" % (term.green('Inserted'), values))


    def get_all_values(self):
        """Renvoie toutes les entrées de la base."""
        return self.db.fingers.find()


    def clear(self):
        """Supprime toutes les données de la collection."""
        self.db.fingers.remove()


def main():
    """Fonction de test"""
    b = DB()
    b.clear()
    values = [
        {'BALISE_3': 56, 'BALISE_2': 50, 'BALISE_1': 39, 'BALISE_5': 61, 'BALISE_4': 63, 'y': 0, 'x': 0},
        {'BALISE_3': 62, 'BALISE_2': 49, 'BALISE_1': 55, 'BALISE_5': 52, 'BALISE_4': 58, 'y': 1, 'x': 0},
        {'BALISE_3': 64, 'BALISE_2': 50, 'BALISE_1': 55, 'BALISE_5': 46, 'BALISE_4': 57, 'y': 2, 'x': 0}
    ]

    b.insert(values)
    b.get_all_values()


if __name__ == "__main__":
    main()

