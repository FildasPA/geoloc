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

fingerprints = {}


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
    global fingerprints

    sleep(0.2)
    ser.write('+++')
    print('+++')
    sleep(1)
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        print('OK')
        sleep(1)
        incomingByte = ''
        ser.write('ATND\r')
        finger = read_beacons(ser)
        if finger:
            print(finger)
            fingerprints = dict(fingerprints.items() + finger.items())
        # ser.write('ATCN\r')


def get_fingerprint(func):
    global fingerprints

    while True:
        send()
        if all(key in fingerprints for key in BEACONS):
            print('ALL: ' + str(fingerprints))
            func(fingerprints)
            fingerprints = {}
            break

def main():
    while True:
        send()


if __name__ == "__main__":
    main()
