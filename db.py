#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import term


URI = 'mongodb://localhost:27017'
DB_NAME = 'geogeloc'


class DB:
    def __init__(self):
        """Initialise la connexion avec la BDD"""
        self.client = pymongo.MongoClient(URI)
        self.db = self.client.get_database(DB_NAME)


    def __del__(self):
        # self.db.close() # Si besoin de fermer la connexion manuellement
        pass

    def insert(self, values):
        """values = {'x': N, 'y': N, 'BALISE_1': N, 'BALISE_2': N, ..., 'BALISE_5': N}"""
        self.db.fingers.insert_one(values)
        print("%s: %s" % (term.green('Inserted'), values))


    def get_all_values(self):
        """Renvoie toutes les valeurs"""
        return self.db.fingers.find()


    def clear(self):
        """Supprime toutes les données de la collection"""
        self.db.fingers.remove()

def main():
    b = DB()
    # values = {"x":"0","y":"0","BALISE_1":"0","BALISE_2":"0","BALISE_3":"0","BALISE_4":"0","BALISE_5":"0"}

    b.clear()
    values = [
        {'BALISE_3': 56, 'BALISE_2': 50, 'BALISE_1': 39, 'BALISE_5': 61, 'BALISE_4': 63, 'y': 0, 'x': 0},
        {'BALISE_3': 62, 'BALISE_2': 49, 'BALISE_1': 55, 'BALISE_5': 52, 'BALISE_4': 58, 'y': 1, 'x': 0},
        {'BALISE_3': 64, 'BALISE_2': 50, 'BALISE_1': 55, 'BALISE_5': 46, 'BALISE_4': 57, 'y': 2, 'x': 0},
        {'BALISE_3': 56, 'BALISE_2': 55, 'BALISE_1': 49, 'BALISE_5': 53, 'BALISE_4': 60, 'y': 3, 'x': 0},
        {'BALISE_3': 53, 'BALISE_2': 54, 'BALISE_1': 54, 'BALISE_5': 53, 'BALISE_4': 53, 'y': 4, 'x': 0},
        {'BALISE_3': 59, 'BALISE_2': 59, 'BALISE_1': 46, 'BALISE_5': 48, 'BALISE_4': 57, 'y': 5, 'x': 0},
        {'BALISE_3': 58, 'BALISE_2': 62, 'BALISE_1': 45, 'BALISE_5': 59, 'BALISE_4': 53, 'y': 6, 'x': 0},
        {'BALISE_3': 50, 'BALISE_2': 58, 'BALISE_1': 51, 'BALISE_5': 61, 'BALISE_4': 56, 'y': 7, 'x': 0},
        {'BALISE_3': 54, 'BALISE_2': 69, 'BALISE_1': 61, 'BALISE_5': 58, 'BALISE_4': 63, 'y': 7, 'x': 1},
        {'BALISE_3': 51, 'BALISE_2': 58, 'BALISE_1': 58, 'BALISE_5': 53, 'BALISE_4': 56, 'y': 6, 'x': 1},
        {'BALISE_3': 54, 'BALISE_2': 59, 'BALISE_1': 65, 'BALISE_5': 64, 'BALISE_4': 57, 'y': 5, 'x': 1},
        {'BALISE_3': 56, 'BALISE_2': 63, 'BALISE_1': 55, 'BALISE_5': 45, 'BALISE_4': 59, 'y': 4, 'x': 1},
        {'BALISE_3': 57, 'BALISE_2': 59, 'BALISE_1': 56, 'BALISE_5': 55, 'BALISE_4': 62, 'y': 3, 'x': 1},
        {'BALISE_3': 56, 'BALISE_2': 56, 'BALISE_1': 54, 'BALISE_5': 45, 'BALISE_4': 64, 'y': 2, 'x': 1},
        {'BALISE_3': 60, 'BALISE_2': 53, 'BALISE_1': 55, 'BALISE_5': 50, 'BALISE_4': 68, 'y': 1, 'x': 1},
        {'BALISE_3': 60, 'BALISE_2': 58, 'BALISE_1': 45, 'BALISE_5': 55, 'BALISE_4': 60, 'y': 0, 'x': 1}
    ]

    b.insert(values)
    b.get_all_values()


if __name__ == "__main__":
    main()

