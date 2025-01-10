"""Meshtastic related commands."""

import json
import logging

import meshtastic
import meshtastic as mesh_pb2
from meshtastic.serial_interface import SerialInterface

# from meshtastic import SerialInterface

logging.basicConfig(level=logging.INFO)


class Mesh:
    def __init__(self, device_path: str = None) -> None:
        """Initialize the Mesh class.

        Args:
            device_path: The path to the Meshtastic device. Autodetect if None.
        """
        self.device_path = None
        self.interface = None

    def connect(self) -> None:
        """Connect to the Meshtastic device."""

        try:
            self.interface = (
                SerialInterface(self.device_path)
                if self.device_path
                else SerialInterface()
            )
            logging.info(
                f"Connected to Meshtastic device. {json.dumps(self.interface.getMyNodeInfo(), indent=4)}"
            )

        except Exception as e:
            logging.info(f"Failed to connect to Meshtastic device: {e}")

    def _on_receive(self, packet) -> None:
        """Callback for handling incoming packets.

        Args:
            packet: The incoming Meshtastic packet.
        """
        try:

            # Extract message if it is a text message.
            if (
                mesh_pb2.Data.Decode(packet.get("decoded", {})).WhichOneof("payload")
                == "text"
            ):
                text_message: str = packet["decoded"]["data"]["text"]
                from_id: str = packet["fromId"]

                logging.info(f"Received message from {from_id}: {text_message}")
            else:

                logging.info("Received non-text packet.")
        except Exception as e:
            logging.info(f"Error handling received packet: {e}")

    def start_listening(self) -> None:
        """Start listening for incoming messages."""

        if not self.interface:
            logging.info("Device is not connected. Please connect first.")
            return

        # Add the on_receive callback.
        self.interface.onReceive = self._on_receive

        logging.info("Listening for incoming messages. Press Ctrl+C to stop.")

        try:

            # Keep the program running to listen for messages.
            while True:
                pass

        except KeyboardInterrupt:
            self.disconnect()
            logging.info("Stopped listening.")

    def disconnect(self) -> None:
        """Disconnect from the Meshtastic device."""

        if self.interface:
            self.interface.close()
            logging.info("Disconnected from Meshtastic device.")
