import struct

from pymunk import Vec2d


def encode_vec2d(vec: Vec2d) -> bytes:
    return struct.pack('<dd', vec.x, vec.y)


def decode_vec2d(data: bytes) -> Vec2d:
    return Vec2d(*struct.unpack('<dd', data))


def encode_joint_list(joints: list[Vec2d]) -> bytes:
    return b''.join(encode_vec2d(joint) for joint in joints)


def decode_joint_list(data: bytes) -> list[Vec2d]:
    return [decode_vec2d(data[i:i + 16]) for i in (0, 16, 32, 48, 64, 80, 96)] # Addresses of the joints
