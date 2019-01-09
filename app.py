#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
import datetime

app = Flask(__name__)

x = -1
y = -1
rssis = {}
date = ''

BEACONS = [
    'BALISE_1',
    'BALISE_2',
    'BALISE_3',
    'BALISE_4',
    'BALISE_5'
]

@app.route('/')
def index():
    return render_template('app.html', x=x, y=y)


@app.route('/setPosition')
def setPosition():
    global x, y, rssis, date
    x = request.args.get('x')
    y = request.args.get('y')
    for beacon in BEACONS:
        if beacon in request.args:
            rssis[beacon] = request.args.get(beacon)
        else:
            rssis[beacon] = 0

    now = datetime.datetime.now()
    date = now.strftime("%H:%M:%S")
    return ''


@app.route('/getPosition')
def getPosition():
    params = '{'
    params += '"x": %s, "y": %s' % (x, y)
    params += ', "date":"%s"' % date
    for beacon in BEACONS:
        if beacon in rssis:
            params += ', "%s": %s' % (beacon, rssis[beacon])

    params += '}'
    return params


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
