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


db = DB()

values = db.get_all_values()

m = matrix.Matrix(columns=['x', 'y',
                           'BALISE_1',
                           'BALISE_2',
                           'BALISE_3',
                           'BALISE_4',
                           'BALISE_5'])

for d in values:
    m.append(d)


def calculate_position(values):
    nearest = m.get_nearest(values, 4)
    x = 0
    y = 0
    for row in nearest:
        x += row['x']
        y += row['y']

    x /= len(nearest)
    y /= len(nearest)

    params = {'x': x, 'y': y}
    for row in nearest:
        requests.get(url='http://10.120.14.37:5000/setPosition', params=params, timeout=5)


def get_position():
    at.get_fingerprint(calculate_position)


def main():
    while True:
        get_position()


if __name__ == "__main__":
    main()
