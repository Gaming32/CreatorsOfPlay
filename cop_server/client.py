from __future__ import annotations

import logging
import socket
from typing import Optional

from cop_common.network import (PacketType, decode_packet, encode_packet,
                                format_address)
from cop_common.player import Player
from cop_common.serializers import decode_joint_list, encode_joint_list


class Client:
    server: Server
    sockobj: socket.socket
    address: tuple
    name: str
    player: Player

    def __init__(self, serv, sock, addr) -> None:
        self.server = serv
        self.sockobj = sock
        self.address = addr
        self.name = format_address(addr)
        self.player = Player()
        logging.info('Client %s connected!', self.name)

    def disconnect(self, reason: str):
        self.sockobj.close()
        self.server.active_players.discard(self)
        logging.info('Client %s disconnected', self.name)
        logging.info('REASON: %s', reason)

    def handle(self):
        try:
            self.sockobj.send(encode_packet(PacketType.UPDATE_JOINTS, encode_joint_list(self.player.joints)))
        except ConnectionError as e:
            self.disconnect(f'{e.__class__.__qualname__}: {e}')
        except Exception:
            logging.error('Exception in client %s', self.name, exc_info=True)

    def kick(self, reason: str = 'Kicked by server operator'):
        self.sockobj.send(encode_packet(PacketType.KICK, reason.encode('utf-8')))
        self.disconnect(f'Kicked: {reason}')


from cop_server.server import Server
