import logging
import socket

from pymunk.vec2d import Vec2d

from cop_client import globvars
from cop_client.player import ClientSidePlayer
from cop_common.network import (DEFAULT_PORT, PacketType, decode_packet, encode_packet,
                                format_address)
from cop_common.serializers import decode_joint_list, decode_level, encode_vec2d


class Client:
    sockobj: socket.socket
    address: tuple
    server_name: str
    player: ClientSidePlayer
    level: dict

    def __init__(self) -> None:
        self.sockobj = None
        self.address = ()
        self.server_name = ''
        self.player = None
        self.level = {}

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
        logging.info('Connected to %s!', self.server_name)
        self.player = ClientSidePlayer()

    def disconnect(self):
        self.sockobj.close()
        logging.info('Successfully disconnected from server!')

    def handle(self):
        self.sockobj.setblocking(False)
        try:
            packet_type, payload = decode_packet(self.sockobj)
        except BlockingIOError:
            return
        finally:
            self.sockobj.setblocking(True)
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
        elif packet_type == PacketType.SEND_LEVEL:
            self.level = decode_level(payload)

    def move(self, movement: Vec2d):
        self.sockobj.setblocking(False)
        try:
            self.sockobj.send(encode_packet(PacketType.PLAYER_MOVE, encode_vec2d(movement)))
        except BlockingIOError:
            logging.warning('Movement packet not sent', exc_info=True)
        self.sockobj.setblocking(True)

