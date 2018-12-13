#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo


class BDD:
    def __init__(self):
        """Initialise la connexion avec la BDD"""
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = client['pymongo_test']


    def __del__(self):
        # self.db.close() # Si besoin de fermer la connexion manuellement
        pass

    def add_fingerprint(values):
        """values = {'x': N, 'y': N, 'BALISE_1': N, 'BALISE_2': N, ..., 'BALISE_5': N}"""
        pass


    def get_all_values():
        """Renvoie toutes les valeurs"""
        pass
