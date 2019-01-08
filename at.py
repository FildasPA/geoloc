#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Les fonctions de ce script permettent de communiquer avec les balises
et de récupérer les informations retournées, dont le RSSI.

Notamment, la fonction get_fingerprint permet de récupérer une empreinte
complète : des messages sont envoyés jusqu'à avoir récupérer un nombre
donné de valeurs pour chaque balise, qui seront ensuite moyennées."""

import serial
from time import sleep
import term

# Nombre de valeurs à récupérer par balise pour constituer une empreinte
n = 5
# Noms des balises à considérer
BEACONS = [
    'BALISE_1',
    'BALISE_2',
    'BALISE_3',
    'BALISE_4',
    'BALISE_5'
]

# Initialise le port série pour communiquer avec les balises
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2)
print(ser.name)


def readline(ser):
    """Lis et retourne une ligne reçue sur le port série"""

    line = ''
    while True:
        byte = ser.read()
        if byte == '\r': # fin de ligne ?
            return line
        line += byte


def read_beacon_infos(ser):
    """Lis et retourne toutes les informations d'une balise."""

    infos = []
    while True:
        line = readline(ser)
        if line == '':
            return infos[-2:]
        infos.append(line)


def read_beacons(ser):
    """"Lis et retourne les informations de toutes les balises."""

    beacons_infos = {}
    while True:
        infos = read_beacon_infos(ser)
        if not infos:
            return beacons_infos
        beacons_infos[infos[-1]] = int(infos[-2], 16)


def send():
    """Envoie la commande 'ATND' aux balises et retourne
    les informations reçues.

    La commande 'ATND' retourne les informations suivantes:
    - adresse MY
    - numéro de série SH (partie haute)
    - numéro de série SL (partie basse)
    - RSSI (force du signal radio)
    - nom du module"""
    ser.write('+++')
    print(term.yellow('+++'))
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        term.clear_previous_line()
        print(term.green('OK'))
        ser.write('ATND\r')
        finger = read_beacons(ser)
        if finger:
            term.clear_previous_line()
            print(finger)
        return finger


def get_fingerprint():
    """Communique avec les balises jusqu'à avoir récupéré au moins n valeurs
    pour chaque balise, puis retourne l'empreinte constituée des moyennes de
    ces valeurs."""
    global n
    rssi_lists = {beacon:list() for beacon in BEACONS}
    # Tant qu'on a pas au moins n valeurs pour chaque balise
    while not all(len(lst) >= n for beacon, lst in rssi_lists.iteritems()):
        # Récupère les RSSI renvoyés par les balises actuellement disponibles
        values = send()
        if values:
            for beacon, rssi in values.iteritems():
                rssi_lists[beacon].append(rssi)

    # Calcule la moyenne des RSSIs pour chaque balise
    fingerprint = {}
    for beacon, lst in rssi_lists.iteritems():
        fingerprint[beacon] = int(sum(lst) / float(len(lst)))

    return fingerprint


def main():
    while True:
        send()


if __name__ == "__main__":
    main()
