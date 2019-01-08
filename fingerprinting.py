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
import time
import term

max_x = 7
max_y = 8

db = DB()


def insert_print(values):
    db.insert(values)


def record(x, y):
    term.print_separator('-')
    print('Doing: (%s, %s)' % (x, y))

    # Met à jour la position du coordinateur sur le serveur
    params = {'x': x, 'y': y}
    try:
        requests.get(url='http://localhost:5000/setPosition', params=params, timeout=5)
    except Exception as e:
        pass

    # Accorde un délai pour positionner le coordinateur
    time.sleep(5)

    # Récupère une empreinte
    fingerprint = at.get_fingerprint()

    fingerprint['x'] = x
    fingerprint['y'] = y

    insert_print(fingerprint)


def main():
    x = 0
    y = 0

    # Effectue un parcours en zigzag
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
