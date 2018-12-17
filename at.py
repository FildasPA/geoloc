import serial
from time import sleep
import db

ser = serial.Serial('/dev/ttyS0', baudrate=9600)


print(ser.name)

finger = {}
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
    sleep(1)
    ser.write('+++')
    sleep(1)
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        # print('+++')
        sleep(1)
        incomingByte = ''
        ser.write('ATND\r')
        return read_beacons(ser)
        # ser.write('ATCN\r')


def main():
    while True:
        send()


if __name__ == "__main__":
    main()
