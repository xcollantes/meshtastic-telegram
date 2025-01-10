from mesh import Mesh

import time
import meshtastic
import meshtastic.tcp_interface
from pubsub import pub


def onReceive(packet, interface):  # called when a packet arrives
    print(f"Received: {packet}")


def onConnection(
    interface, topic=pub.AUTO_TOPIC
):  # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("hello mesh")


pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")
# interface = meshtastic.serial_interface.SerialInterface()

while True:
    time.sleep(10000)
interface.close()
