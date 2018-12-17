import serial
from time import sleep
import db

ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2)

BEACONS = [
    'BALISE_1',
    'BALISE_2',
    'BALISE_3',
    'BALISE_4',
    'BALISE_5'
]


print(ser.name)

fingers = {}
bdd = db.BDD()


def readline(ser):
    res = ''
    while True:
        byte = ser.read()
        if byte == '\r':
            return res
        res += byte


def read_beacon_infos(ser):
    global finger

    infos = []
    while True:
        line = readline(ser)
        if line == '':
            return infos[-2:]
        infos.append(line)


def read_beacons(ser):
    beacons_infos = {}
    while True:
        infos = read_beacon_infos(ser)
        if not infos:
            return beacons_infos
        beacons_infos[infos[-1]] = infos[-2]


def send():
    global fingers

    sleep(0.2)
    ser.write('+++')
    sleep(1)
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        print('+++')
        sleep(1)
        incomingByte = ''
        ser.write('ATND\r')
        finger = read_beacons(ser)
        if finger:
            print(finger)
            fingers = dict(fingers.items() + finger.items())
        if all(key in fingers for key in BEACONS):
            print('ALL: ' + str(fingers))
            fingers['x'] = raw_input('x ? ')
            fingers['y'] = raw_input('y ? ')
            bdd.add_fingerprint(fingers)
            fingers = {}
        # ser.write('ATCN\r')


def main():
    while True:
        send()


if __name__ == "__main__":
    main()
