#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ce script permet de réaliser la cartographie radio de la salle.
Pour chaque position donnée, des valeurs RSSI correspondant à chaque balise sont relevées. Cette empreinte est associée à une position (x,y) puis enregistrée
dans une bdd.

position (x,y). une empreinte est relevée, associée à une position
(x, y) et enregistrée dans
le module XBee commnique avec les balises jusqu'à
avoir récupéré le RSSI associé à chacune d'elles. Cette empreinte (fingerprint)
est ensuite enregistrée dans une bdd."""

import requests

from db import DB
import at

max_x = 8
max_y = 8

db = DB()


def insert_print(values):
    db.insert(values)


def record(x, y):
    print('Doing: (%s, %s)' % (x, y))

    params = {'x': x, 'y': y}
    try:
        requests.get(url='http://localhost:5000/setPosition', params=params, timeout=5)
    except Exception as e:
        pass

    avg_fingerprint = {}
    n = 5
    for i in range(0, n+1):
        print('RECORDING (%s, %s) #%s' % (x, y, n))
        fingerprint = at.get_fingerprint({'x':x, 'y':y})

        for key, value in fingerprint.iteritems():
            if key not in avg_fingerprint:
                avg_fingerprint[key] = value
            else:
                avg_fingerprint[key] += value

    for key, value in avg_fingerprint.iteritems():
        if key != 'x' and key != 'y':
            avg_fingerprint[key] /= 5

    print('RECORDED: %s' % avg_fingerprint)
    insert_print(avg_fingerprint)



def main():
    x = 5
    y = 2

    while x < max_x:
        if x % 2 == 0:
            while y < max_y:
                record(x, y)
                y += 1
            y = max_y - 1
        else:
            while y >= 0:
                record(x, y)
                y -= 1
            y = 0
        x += 1



if __name__ == "__main__":
    main()
