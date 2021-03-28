import logging
import socket

from cop_client import globvars
from cop_client.player import ClientSidePlayer
from cop_common.network import (DEFAULT_PORT, PacketType, decode_packet,
                                format_address)
from cop_common.serializers import decode_joint_list


class Client:
    sockobj: socket.socket
    address: tuple
    server_name: str
    player: ClientSidePlayer

    def __init__(self) -> None:
        self.sockobj = None
        self.address = ()
        self.server_name = ''
        self.player = None

    def connect(self, address, port: int = DEFAULT_PORT) -> bool:
        if ':' in address:
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
        self.address = (address, port)
        self.server_name = format_address(self.address)
        self.sockobj = socket.socket(family)
        logging.info('Conncecting to %s...', self.server_name)
        try:
            self.sockobj.connect(self.address)
        except Exception:
            logging.error('Failed to connect to %s', self.server_name, exc_info=True)
            return False
        self.sockobj.setblocking(False)
        logging.info('Connected to %s!', self.server_name)
        self.player = ClientSidePlayer()

    def disconnect(self):
        self.sockobj.close()
        logging.info('Successfully disconnected from server!')

    def handle(self):
        try:
            packet_type, payload = decode_packet(self.sockobj)
        except BlockingIOError:
            return
        if packet_type == PacketType.INVALID_PACKET:
            logging.warning('Recieved invalid packet from server: %r', payload)
        elif packet_type == PacketType.EMPTY_PACKET:
            logging.debug('RAW DATA: %r', payload)
        elif packet_type == PacketType.KICK:
            reason = payload.decode('utf-8')
            logging.info('Kicked from server for reason: %s', reason)
            self.disconnect()
        elif packet_type == PacketType.UPDATE_JOINTS:
            joints = decode_joint_list(payload)
            self.player.joints[:] = joints
