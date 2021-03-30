from __future__ import annotations

import logging
import socket
from typing import Optional

from pymunk.body import Body
from pymunk.constraints import PinJoint, PivotJoint
from pymunk.shapes import Segment
from pymunk.vec2d import Vec2d

from cop_common.network import (PacketType, decode_packet, encode_packet,
                                format_address)
from cop_common.player import Player
from cop_common.serializers import decode_joint_list, decode_vec2d, encode_joint_list, encode_level


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
        self.start()

    def start(self):
        self.sockobj.send(encode_packet(PacketType.SEND_LEVEL, encode_level(self.server.level)))
        self.player.joints = [
            Vec2d(0, 0),
            Vec2d(-50, -50),
            Vec2d(50, -50),
            Vec2d(0, 50),
            Vec2d(-25, 25),
            Vec2d(25, 25),
            Vec2d(0, 75),
        ]
        segs = self.player.segments
        bodies = self.player.bodies
        pins = self.player.pins
        joints = self.player.joints
        for i in range(3): # Create the body and arms
            bodies.append(Body(0, 100))
            bodies[i].position = tuple(joints[3])
        segs.append(Segment( # Body segment
            bodies[0],
            tuple(joints[0]),
            tuple(joints[6]),
            5.0
        ))
        segs.append(Segment( # Left arm segment
            bodies[1],
            tuple(joints[3]),
            tuple(joints[4]),
            5.0
        ))
        segs.append(Segment( # Right arm segment
            bodies[2],
            tuple(joints[3]),
            tuple(joints[5]),
            5.0
        ))
        segs[0].friction = 1
        segs[0].mass = 100
        segs[1].friction = 1
        segs[1].mass = 8
        segs[2].friction = 1
        segs[2].mass = 8
        pins.append(PinJoint( # Connect the body to the left arm
            bodies[0], bodies[1],
            tuple(joints[3]), tuple(joints[3])
        ))
        pins[0].collide_bodies = False
        pins.append(PinJoint( # Connect the body to the right arm
            bodies[0], bodies[2],
            tuple(joints[3]), tuple(joints[3])
        ))
        pins[1].collide_bodies = False
        for i in range(2): # Create the legs
            bodies.append(Body(0, 100))
            bodies[i].position = tuple(joints[0])
        segs.append(Segment( # Left leg segment
            bodies[3],
            tuple(joints[0]),
            tuple(joints[1]),
            5.0
        ))
        segs.append(Segment( # Right leg segment
            bodies[4],
            tuple(joints[0]),
            tuple(joints[2]),
            5.0
        ))
        segs[3].friction = 1
        segs[3].mass = 8
        segs[4].friction = 1
        segs[4].mass = 8
        pins.append(PinJoint( # Connect the body to the left arm
            bodies[0], bodies[3],
            tuple(joints[0]), tuple(joints[0])
        ))
        pins[2].collide_bodies = False
        pins.append(PinJoint( # Connect the body to the right arm
            bodies[0], bodies[4],
            tuple(joints[0]), tuple(joints[0])
        ))
        pins[3].collide_bodies = False
        self.server.space.add(*bodies, *segs, *pins)

    def disconnect(self, reason: str):
        self.sockobj.close()
        self.server.active_players.discard(self)
        self.server.space.remove(*self.player.bodies, *self.player.segments, *self.player.pins)
        logging.info('Client %s disconnected', self.name)
        logging.info('REASON: %s', reason)

    def handle(self):
        joints = self.player.joints
        bod0 = self.player.bodies[0].position
        bod1 = self.player.bodies[3].position
        seg0 = self.player.segments[0]
        seg1 = self.player.segments[1]
        seg2 = self.player.segments[2]
        seg3 = self.player.segments[3]
        seg4 = self.player.segments[4]
        joints[3] = seg1.a + bod0
        joints[0] = seg0.a + bod0
        joints[6] = seg0.b + bod0
        joints[4] = seg1.b + bod0
        joints[5] = seg2.b + bod0
        joints[1] = seg3.b + bod1
        joints[2] = seg4.b + bod1
        try:
            self.sockobj.send(encode_packet(PacketType.UPDATE_JOINTS, encode_joint_list(joints)))
        except ConnectionError as e:
            self.disconnect(f'{e.__class__.__qualname__}: {e}')
        except Exception:
            logging.error('Exception in client %s', self.name, exc_info=True)
        self.sockobj.setblocking(True)
        try:
            packet_type, payload = decode_packet(self.sockobj)
        except BlockingIOError:
            return
        finally:
            self.sockobj.setblocking(True)
        print(packet_type)
        if packet_type == PacketType.PLAYER_MOVE:
            movement = decode_vec2d(payload)
            self.player.bodies[0].apply_impulse_at_local_point(movement)

    def kick(self, reason: str = 'Kicked by server operator'):
        self.sockobj.send(encode_packet(PacketType.KICK, reason.encode('utf-8')))
        self.disconnect(f'Kicked: {reason}')


from cop_server.server import Server
