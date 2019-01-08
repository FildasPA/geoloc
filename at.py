#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Les fonctions de ce script permettent de communiquer avec les balises et de
récupérer les informations retournées, dont le RSSI.

Notamment, la fonction get_fingerprint permet de récupérer une empreinte
complète : des messages sont envoyés aux balises jusqu'à avoir récupérer les informations de toutes les balises avant que l'ensemble de ces informations ne
soit retourné."""

import serial
from time import sleep
import term

ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2)

BEACONS = [
    'BALISE_1',
    'BALISE_2',
    'BALISE_3',
    'BALISE_4',
    'BALISE_5'
]


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
    """Envoie un message aux balises et ajoute leurs réponses à fingerprints"""

    global fingerprints

    ser.write('+++')
    print(term.yellow('+++'))
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        term.clear_previous_line()
        print(term.green('OK'))
        incomingByte = ''
        ser.write('ATND\r')
        finger = read_beacons(ser)
        if finger:
            term.clear_previous_line()
            print(finger)
        return finger
            # fingerprints = dict(fingerprints.items() + finger.items())


def get_fingerprint():
    rssi_lists = {beacon:list() for beacon in BEACONS}
    n = 5
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
