import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0')
ser.baudrate = 115200
print(ser.name)

while True:
    sleep(1)
    #print('writing +++')
    ser.write('+++')
    sleep(1)

    incomingByte = ser.read(size=2);
    # print('read something')
    # print(incomingByte)
    if (incomingByte == 'OK'):
        sleep(1)
        # ser.write('ATIDC133\r')
        incomingByte = ''
        ser.write('ATND\r')
        res = ''
        while True:
            incomingByte = ser.read()
            #print(repr('Lu: %s' % incomingByte))
            if incomingByte == '\r' and res == '\r':
                break
            res += incomingByte
            #print('res: %s' % repr(res))

            if incomingByte == '\r' and res != '\r':
                print(repr(res))
                res = ''
        print('fin de la boucle!')

        #incomingByte = ser.read(size=10);
        #print(incomingByte)
        # sleep(1)
        # ser.write('ATWR\r')
        # sleep(1)
        # ser.write('ATCN\r')

