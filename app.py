#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ce script permet de lancer un mini-serveur.
Il dispose de trois pages :
- un index '/' sur lequel est affiché un plan de la pièce où l'on doit
géolocaliser notre objet
- une page '/setPosition' qui reçoit en paramètre les coordonnées x et y de
l'objet, l'heure à laquelle l'objet a été géolocaliser ainsi que les valeurs
RSSI associées à l'empreinte relevée
- une page '/getPosition' qui retourne au format JSON les dernières informations de géopositionnement reçues"""

from flask import Flask
from flask import render_template
from flask import request
import datetime

# Initialise le serveur
app = Flask(__name__)

# Coordonnées par défaut de l'objet
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
    """Retourne le plan de la salle avec l'objet à localiser, l'emplacement
    des balises, etc."""
    return render_template('app.html', x=x, y=y)


@app.route('/setPosition')
def setPosition():
    """Met à jour les coordonnées de l'objet et les valeurs RSSI de l'empreinte.
    Ajoute également la date à laquelle ces informations ont été reçues."""
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
    """Retourne les dernières informations de géopositionnement reçues par
    le serveur au format JSON.
    L'information retournée est de la forme:
    {"x": X, "y": Y, "date": "hh:mm:ss", "BALISE1": RSSI1, "BALISE2": RSSI2, ...}"""
    infos = '{'
    infos += '"x": %s, "y": %s' % (x, y)
    infos += ', "date":"%s"' % date
    for beacon in BEACONS:
        if beacon in rssis:
            infos += ', "%s": %s' % (beacon, rssis[beacon])

    infos += '}'
    return infos


if __name__ == '__main__':
    """Démarre le serveur sur le port 5000.
    '0.0.0.0' permet de le rendre accessible par d'autres PC"""
    app.run(debug=True, host='0.0.0.0', port=5000)
