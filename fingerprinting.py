#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ce script permet d'effectuer la cartographie radio d'une salle.
Pour chaque position donnée, des valeurs RSSI correspondant à chaque balise sont
relevées. Cet ensemble de RSSI constitue une "empreinte", qui est associée à
une position (x,y) puis enregistrée dans une bdd."""

import requests
import time

from db import DB
import at
import term


# Initialise la bdd pour sauvegarder les empreintes
db = DB()


def record(x, y):
    """Relève une empreinte à une position donnée et l'enregistre dans la
    base de données."""
    term.print_separator('-')
    print('Doing: (%s, %s)' % (x, y))

    # Met à jour la position du coordinateur sur le serveur (permet de vérifier
    # graphiquement qu'on est à la bonne position)
    params = {'x': x, 'y': y}
    try:
        requests.get(url='http://localhost:5000/setPosition',
                     params=params, timeout=5)
    except Exception as e:
        pass

    # Accorde un délai pour positionner le coordinateur
    time.sleep(5)

    # Relève une empreinte
    fingerprint = at.get_fingerprint()

    # Associe les coordonnées à l'empreinte
    fingerprint['x'] = x
    fingerprint['y'] = y

    # Insère une nouvelle entrée dans la bdd
    db.insert(fingerprint)


def main():
    # Coordonnées de départ
    x = 0
    y = 0
    # Nombre de positions à relever sur chaque axe x, y
    max_x = 7
    max_y = 8

    # Effectue un parcours en zigzag dans la salle (plus pratique)
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
