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


def encode_level(level: dict) -> bytes:
    pts: list[int] = level['data']
    return b''.join(pt.to_bytes(4, 'little', signed=True) for pt in pts)


def decode_level(data: bytes) -> dict:
    return {
        'data': [int.from_bytes(data[pti:pti+4], 'little', signed=True) for pti in range(0, len(data), 4)]
    }
