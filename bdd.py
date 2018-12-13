#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo


class BDD:
    def __init__(self):
        self.open()


    def open():
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['pymongo_test']


    def add_fingerprinting():
        pass


    def get_():
        pass


    def get_nearest(k=4):
        pass
