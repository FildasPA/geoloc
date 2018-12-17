import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', baudrate=115200)


print(ser.name)

finger = {}


def add_infos(node_id, rssi):
    if not finger[node_id]:
        finger[node_id] = rssi


def readline(ser):
    res = ''
    # print('Reading line')
    while True:
        byte = ser.read()
        if byte == '\r':
            return res
        res += byte

def read_beacon_infos(ser):
    global finger

    infos = []
    # print('Reading beacon')
    while True:
        line = readline(ser)
        if line == '':
            add_infos(infos[-1], infos[-2])
            return infos[-2:]
        # print(line)
        infos.append(line)

def read_beacons(ser):
    beacons_infos = []
    # print('Reading beacons infos')
    while True:
        infos = read_beacon_infos(ser)
        if not infos:
            return beacons_infos
        beacon, rssi
        beacons_infos.append({'beacons': infos[-1], 'rssi': infos[-2]})


def send():
    sleep(1)
    ser.write('+++')
    sleep(1)
    incomingByte = ser.read(size=3)
    if (incomingByte == 'OK\r'):
        print('+++')
        sleep(1)
        incomingByte = ''
        ser.write('ATND\r')
        print(read_beacons(ser))
        # ser.write('ATCN\r')


def main():
    while True:
        send()


if __name__ == "__main__":
    main()
