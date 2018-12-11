from digi.xbee.devices import XBeeDevice
from digi.xbee.packets.base import DictKeys
from time import sleep

PORT = "/dev/ttyS0"
BAUD_RATE = 9600
DATA_TO_SEND = 'mdr'
REMOTE_NODE_ID = 'BALISE_1'

def send_data():
    print("Sending data...")

    xbee_network = device.get_network()
    remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

    if remote_device is None:
        print('Could not find the remote device')
        exit(1)

    print("Sending data to %s >> %s" % (remote_device.get_64bit_addr(), DATA_TO_SEND))
    device.send_data(remote_device, DATA_TO_SEND)
    print('Success')

def packet_received_callback(packet):
    packet_dict = packet.to_dict()
    api_data = packet_dict[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
    data = api_data[DictKeys.RF_DATA]
    rssi = api_data[DictKeys.RSSI]
    address16 = api_data[DictKeys.X16BIT_ADDR]
    print("from: {}, RSSI: {}, Data: {}\n".format(address16, rssi, data.decode()))
    if data == bytearray(DATA_TO_SEND, 'utf-8'):
        print("Reçu notre paquet !")

def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        device.add_packet_received_callback(packet_received_callback)

        while True:
            send_data()
            sleep(2)



        # print("Waiting for data...\n")

        # input()

    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    main()
