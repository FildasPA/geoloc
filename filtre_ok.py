from digi.xbee.devices import XBeeDevice
from digi.xbee.packets.base import DictKeys
from time import sleep
import pymongo

# Réseau
PORT = "/dev/ttyS0"
BAUD_RATE = 9600
DATA_TO_SEND = 'mdr'
WAIT = 2 # in seconds
# Balises
REMOTE_NODE_ID = 'BALISE_1'
REMODE_DEVICES = {
    'BALISE_1': '',
    # 'BALISE_2': '',
    # 'BALISE_3': '',
    # 'BALISE_4': '',
    # 'BALISE_5': ''
}

# Database
BDD_CLIENT = 'mongodb://localhost:27017'
BDD_NAME = 'pymongo_test'


def send_data(remote_device, device):
    """Envoie un message à une balise."""
    print("Sending data to %s >> %s" % (remote_device.get_64bit_addr(), DATA_TO_SEND))
    device.send_data_async(remote_device, DATA_TO_SEND)


def packet_received_callback(packet):
    """Réceptionne la réponse d'une balise."""
    packet_dict = packet.to_dict()
    api_data = packet_dict[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
    if DictKeys.RSSI in api_data:
        data = api_data[DictKeys.RF_DATA]
        rssi = api_data[DictKeys.RSSI]
        address16 = api_data[DictKeys.X16BIT_ADDR]
        print("Received response from: {}, RSSI: {}, Data: {}".format(address16, rssi, data.decode()))
        if data.decode() == DATA_TO_SEND:
            print("C'est notre paquet !")


def add_record(beacon, rssi):
    """Enregistre le RSSI d'une balise pour une position donnée."""
    pass

def main():

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

        if remote_device is None:
            print('Could not find the remote device')
            exit(1)

        client = pymongo.MongoClient(BDD_CLIENT)
        db = client[BDD_NAME]

        device.add_packet_received_callback(packet_received_callback)

        while True:
            send_data(remote_device, device)
            sleep(WAIT)

    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    main()
