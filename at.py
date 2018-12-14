import serial

ser = serial.Serial('/dev/ttyS0')
ser.baudrate = 115200
print(ser.name)

while True:
    sleep(1)
    ser.write('+++')
    sleep(1)

    incomingByte = ser.read();

    if (incomingByte == '\r'):
        sleep(1)
        # ser.write('ATIDC133\r')
        ser.write('ATND\r')
        # sleep(1)
        # ser.write('ATWR\r')
        # sleep(1)
        # ser.write('ATCN\r')
