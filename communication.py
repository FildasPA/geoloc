from digi.xbee.devices import XBeeDevice

PORT = '/dev/ttyS0'
BAUD_RATE = 9600
DATA_TO_SEND = '+++atdb'
REMOTE_NODE_ID = 'BALISE_1'

def main():
        device = XBeeDevice(PORT, BAUD_RATE)

        try:
            device.open()

            xbee_network = device.get_network()
            remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

            if remote_device is None:
                print('Could not find the remote device')
                exit(1)

            print("Sending data to %s >> %s" % (remote_device.get_64bit_addr(), device.send_data(remote_device, DATA_TO_SEND)))

            # print("Success")

            #device.flush_queues()
            #print("Waiting for data...\n")

            #while True:
            def data_receive_callback(xbee_message):
                #xbee_message = device.read_data()
                #if xbee_message is not None:
                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), xbee_message.data.decode()))
                print(xbee_message.remote_device.__dict__)


            def data_receive_callback(xbee_message):
                #xbee_message = device.read_data()
                #if xbee_message is not None:
                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_address, xbee_message.data.decode()))
                print(xbee_message.remote_device.__dict__)

            device.add_data_received_callback(data_receive_callback)
            print("Waiting for data...\n")
            input()

        finally:
            if device is not None and device.is_open():
                device.close()

if __name__ == '__main__':
    main()
