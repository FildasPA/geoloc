#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        requests.get(url='http://10.120.14.37:5000/setPosition', params=params, timeout=5)
    except requests.exceptions.Timeout:
        pass

    at.get_fingerprint(insert_print, x, y)

def main():
    global x, y

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
