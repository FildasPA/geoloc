#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from db import DB
import at
from matrix import Matrix


db = DB()

values = db.get_all_values()

for d in values:
    matrix.append(d)

print(matrix)

def calculate_position(values):
    values = {k:v for values}
    nearest = matrix.get_nearest(values)
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
    at.get_fingerprint(calculate_position, 0, 0)


def main():
    while True:
        get_position()


if __name__ == "__main__":
    main()
