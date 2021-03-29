from __future__ import annotations

import json
import logging
import socket
import threading

from pygame.time import Clock
from pymunk import Space, Body
import pymunk
from pymunk.shapes import Segment

from cop_common.network import DEFAULT_PORT, format_address
from cop_server.consts import TICK_RATE


class Server:
    sockobj: socket.socket
    active_players: set[Client]
    display_address: str
    stop_all: bool

    # PyMunk stuff
    space: Space
    level: dict

    def __init__(self, port: int = DEFAULT_PORT) -> None:
        self.sockobj = socket.create_server(('', port), family=socket.AF_INET6, dualstack_ipv6=True)
        self.active_players = set()
        self.display_address = ''
        # PyMunk setup
        self.space = Space(threaded=True)
        self.space.threads = 2
        self.space.gravity = (0, -200)
        self.load_level('level')

    def load_level(self, name):
        with open(name + '.json') as fp:
            self.level = json.load(fp)
        lines = self.level['data']
        body = Body(body_type=pymunk.Body.STATIC)
        body.position = (0, 0)
        segments = []
        for i in range(0, len(lines), 4):
            segment = Segment(body, (lines[i], lines[i + 1]), (lines[i + 2], lines[i + 3]), 5)
            segment.friction = 1
            segments.append(segment)
        self.space.add(body, *segments)

    def gameloop(self):
        clock = Clock()
        while not self.stop_all:
            tps = 1 / (clock.tick(TICK_RATE) / 1000)
            self.space.step(0.05)
            for client in tuple(self.active_players):
                client.handle()
        logging.info('Kicking online players...')
        for client in tuple(self.active_players):
            client.kick('Server stopped')

    def listen(self):
        self.stop_all = False
        self.sockobj.listen()
        self.display_address = format_address(self.sockobj.getsockname())
        logging.info('Server listening on %s', self.display_address)
        stop_reason = ''
        try:
            threading.Thread(target=self.gameloop, name='GameManager').start()
            while True:
                try:
                    sock, addr = self.sockobj.accept()
                    self.active_players.add(Client(self, sock, addr))
                except Exception as e:
                    logging.error(f'Exception in connection accept', exc_info=True)
        except KeyboardInterrupt:
            stop_reason = ' by ^C'
        self.stop_all = True
        logging.info('Server stopped%s...', stop_reason)


from cop_server.client import Client
