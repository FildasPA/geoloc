#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from db import DB
import at


max_x = 3
max_y = 3

URL = 'http://10.120.14.37:5000/'

db = DB()


def insert_print(values):
    fingerprints['x'] = raw_input('x ? ')
    fingerprints['y'] = raw_input('y ? ')

    db.insert_print(values)


def main():
    global x, y

    for y in range(max_y):
        for x in range(max_x):
            print('Doing: (%s, %s)' % (x, y))

            params = {'x': x, 'y': y}
            requests.get(url=URL, params=params)

            at.send(insert_print)

            requests.get(url='10.120.13.52')


if __name__ == "__main__":
    main()
