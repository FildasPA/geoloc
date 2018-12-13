#!/usr/bin/python
#-*- coding: utf-8 -*-

from digi.xbee.devices import XBeeDevice
from digi.xbee.packets.base import DictKeys

# Réseau
PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# Balises
REMOTE_DEVICES = {
    'BALISE_1': '',
}

class Sender():

    def __init__(self):
        """Initialise le réseau et établit une connexion avec les balises"""

        print('Initializing network...')

        self.device = XBeeDevice(PORT, BAUD_RATE)
        self.remote_devices = []

        try:
            self.device.open()
        except (TimeoutException, InvalidOperatingModeException, XBeeException) as e:
            print('Can not open XBeeDevice network. Exit')
            exit(1)
        else:
            print('Network opened')

        # Initialise le réseau
        self.xbee_network = self.device.get_network()
        self.discover_devices()

        # Ajoute un rappel lors de la réception d'un paquet
        self.device.add_packet_received_callback(self.packet_received_callback)


    def discover_devices(self):
        # Etablit une connexion avec les balises voulues
        for node_id, adress in REMOTE_DEVICES.iteritems():
            REMOTE_DEVICES[node_id] = connect_remote_device(node_id)


    def __del__(self):
        if self.device is not None and self.device.is_open():
            self.device.close()


    def connect_remote_device(self, remote_node_id):
        try:
            remote_device = self.xbee_network.discover_device(remote_node_id)
        except (TimeoutException, XBeeException,
                InvalidOperatingModeException, ATCommandException,
                ValueError) as e:
            print('Could not discover %s' % remote_node_id)
            return ''
        else:
            if remote_device is None:
                print('Could not find the remote device')
                return ''
            else:
                self.remote_devices.append(remote_device)
                # https://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html#digi.xbee.devices.XBeeDevice.get_16bit_addr
                return remote_device.get_16bit_addr()


    def packet_received_callback(packet):
        """Réceptionne la réponse d'une balise."""
        api_data = packet.to_dict()[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
        if DictKeys.RSSI in api_data:
            data = api_data[DictKeys.RF_DATA]
            rssi = api_data[DictKeys.RSSI]
            address16 = api_data[DictKeys.X16BIT_ADDR]
            print("Received response from: {}, RSSI: {}, Data: {}".format(address16, rssi, data.decode()))
            if data.decode() == DATA_TO_SEND:
                print("C'est notre paquet !")
                # https://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html#digi.xbee.devices.DigiPointNetwork.get_device_by_16
                 # get_device_by_16(x16bit_addr).get_node_id()


    def send_data(remote_device, device):
        """Envoie un message à une balise."""
        # print("Sending data to %s >> %s" % (remote_device.get_64bit_addr(), DATA_TO_SEND))
        device.send_data_async(remote_device, DATA_TO_SEND)
