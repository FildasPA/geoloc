#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ce script permet de géolocaliser l'objet.
A chaque itération, une empreinte est relevée et comparée à celles stockées dans
la bdd remplie lors de la phase de fingerprinting.
La position de l'objet est calculée en faisant la moyenne des k positions dont
les empreintes correspondantes sont les plus similaires (et qui sont sensées
correspondre aux positions les plus proches)."""

import requests

from db import DB
import at
import matrix

BEACONS = [
    'BALISE_1',
    'BALISE_2',
    'BALISE_3',
    'BALISE_4',
    'BALISE_5'
]

columns = ['x', 'y']
columns.extend(BEACONS)
# Définie une matrice avec les colonnes 'x' et 'y' ainsi qu'une colonne par balise
m = matrix.Matrix(columns=columns)


db = DB()
# Récupère toutes les entrées dans la base de données et les insère dans la matrice
for d in db.get_all_values():
    m.append(d)


def refresh_position():
    global BEACONS

    # Relève une nouvelle empreinte
    fingerprint = at.get_fingerprint()
    print('fingerprint: %s' % fingerprint)

    # Détermine les 4 empreintes les plus similaires à l'empreinte relevée
    nearest = m.get_nearest(fingerprint, 4)

    # Calcule la moyenne des positions de ces empreintes
    x = 0.0
    y = 0.0
    for row in nearest:
        x += row['x']
        y += row['y']
    x /= len(nearest)
    y /= len(nearest)

    # Prépare la requête à envoyer au serveur
    # Envoie les valeurs RSSI relevées et les coordonnées déterminées
    params = {'x': x, 'y': y}
    for beacon in BEACONS:
        params[beacon] = fingerprint[beacon]

    # Met à jour la position de l'objet sur le serveur
    try:
        requests.get(url='http://localhost:5000/setPosition',
                     params=params, timeout=5)
    except Exception as e:
        pass


def main():
    while True:
        refresh_position()


if __name__ == "__main__":
    main()
