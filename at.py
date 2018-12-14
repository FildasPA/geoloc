import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0')
ser.baudrate = 115200
print(ser.name)

def readline(ser):
    res = ''
    while True:
        byte = ser.read()
        if byte == '\r':
            return res
        res += byte

def read_beacon_infos(ser):
    infos = []
    while True:
        line = readline(ser)
        if line == '':
            return infos
        print(line)
        infos.append(line)

def read_beacons(ser):
    beacons_infos = []
    while True:
        infos = read_beacon_infos(ser)
        if not infos:
            return beacons_infos
        beacons_infos.append(infos)


while True:
    sleep(1)
    ser.write('+++')
    sleep(1)

    incomingByte = ser.read(size=2);

    if (incomingByte == 'OK'):
        print('Initialized!')
        sleep(1)
        incomingByte = ''
        ser.write('ATND\r')

        read_beacons_infos(ser)
