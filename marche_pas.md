#### Partie qui ne fonctionne pas
Connexion entre les XBee

[](https://michael.bouvy.net/blog/en/2013/04/02/raspberry-pi-xbee-uart-serial-howto/)

Sur Raspberry :

```
sudo apt-get install at
sudo apt-get install minicom
```

__Port série__ /dev/ttyAMA0

ls -l /dev | grep serial

Raspberry :


# Discover devices Aynchrone

```python
    def discover_devices(self):
        """Code original :
        https://github.com/digidotcom/python-xbee/blob/master/examples/network/DiscoverDevicesSample/DiscoverDevicesSample.py
        """
        self.xbee_network.set_discovery_timeout(15)
        self.xbee_network.clear()

        # Callback for discovered devices.
        def callback_device_discovered(remote):
            print("Device discovered: %s" % remote)
            if remote.get_node_id() is in REMOTE_DEVICES.keys():
                REMOTE_DEVICES[remote.get_node_id()] = remote.get_16bit_addr()

        # Callback for discovery finished.
        def callback_discovery_finished(status):
            if status == NetworkDiscoveryStatus.SUCCESS:
                print("Discovery process finished successfully.")
            else:
                print("There was an error discovering devices: %s" % status.description)

        self.xbee_network.add_device_discovered_callback(callback_device_discovered)
        self.xbee_network.add_discovery_process_finished_callback(callback_discovery_finished)

        self.xbee_network.start_discovery_process()
        print("Discovering beacons...")

        while self.xbee_network.is_discovery_running():
            time.sleep(0.1)
```
