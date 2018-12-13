#!/usr/bin/python
#-*- coding: utf-8 -*-

"""Fonctions permettant de communiquer avec les balises."""

from digi.xbee.devices import XBeeDevice
from digi.xbee.packets.base import DictKeys


# Réseau
PORT = "/dev/ttyS0"
BAUD_RATE = 9600
DISCOVERY_TIMEOUT = 5 # in seconds

# Balises
REMOTE_DEVICES = [
    'BALISE_1'
    'BALISE_2'
    'BALISE_3'
    'BALISE_4'
    'BALISE_5'
]

# Paquets
DATA_TO_SEND = 'mdr'
WAIT = 2 # in seconds


class Sender():

    def __init__(self):
        self.initialize_network()
        self.values = {}


    def initialize_network(self):
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
        self.xbee_network.set_discovery_timeout(DISCOVERY_TIMEOUT)

        # Etablit une connexion avec les balises voulues
        for node_id, adress in REMOTE_DEVICES.iteritems():
            connect_remote_device(node_id)
        # https://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html#digi.xbee.devices.XBeeDevice.get_16bit_addr

        # Ajoute un rappel lors de la réception d'un paquet
        self.device.add_packet_received_callback(self.packet_received_callback)


    def __del__(self):
        if self.device is not None and self.device.is_open():
            self.device.close()


    def clear_values(self):
        self.values.clear()


    def connect_remote_device(self, remote_node_id):
        try:
            remote_device = self.xbee_network.discover_device(remote_node_id)
        except (TimeoutException, XBeeException,
                InvalidOperatingModeException, ATCommandException,
                ValueError) as e:
            print('Could not discover %s' % remote_node_id)
        else:
            if remote_device is None:
                print('Could not discover %s' % remote_node_id)
            else:
                self.remote_devices.append(remote_device)


    def packet_received_callback(self, packet):
        """Réceptionne la réponse d'une balise."""
        api_data = packet.to_dict()[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
        if DictKeys.RSSI in api_data:
            data = api_data[DictKeys.RF_DATA]
            rssi = api_data[DictKeys.RSSI]
            address16 = api_data[DictKeys.X16BIT_ADDR]
            print("Received response from: {}, RSSI: {}, Data: {}".format(address16, rssi, data.decode()))
            if data.decode() == DATA_TO_SEND:
                print("C'est notre paquet !")
                node = self.xbee_network.get_device_by_16(addres16).get_node_id()
                self.values[node] = rssi
                # https://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html#digi.xbee.devices.DigiPointNetwork.get_device_by_16


    def send_data(self, remote_device, device):
        """Envoie un message à une balise."""
        device.send_data_async(remote_device, DATA_TO_SEND)
