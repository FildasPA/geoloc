#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo


URI = 'mongodb://localhost:27017'
DB = 'defi'


class BDD:
    def __init__(self):
        """Initialise la connexion avec la BDD"""
        self.client = pymongo.MongoClient(URI)
        self.db = self.client.get_database(DB)


    def __del__(self):
        # self.db.close() # Si besoin de fermer la connexion manuellement
        pass

    def add_fingerprint(self, values):
        """values = {'x': N, 'y': N, 'BALISE_1': N, 'BALISE_2': N, ..., 'BALISE_5': N}"""
        self.db.fingers.insert_one(values).inserted_id
        print("Valeur ajoutée !")


    def get_all_values(self):
        """Renvoie toutes les valeurs"""
        return self.db.fingers.find()

b = BDD()
values = {"x":"0","y":"0","BALISE_1":"0","BALISE_2":"0","BALISE_3":"0","BALISE_4":"0","BALISE_5":"0"}
b.add_fingerprint(values)
b.get_all_values()
