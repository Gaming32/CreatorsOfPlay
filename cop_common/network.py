import enum
from socket import socket


class PacketType(enum.IntEnum):
    INVALID_PACKET = -1
    EMPTY_PACKET = 0
    KICK = 1
    UPDATE_JOINTS = 2


DEFAULT_PORT: int = 2677
TYPE_LENGTH: int = 2
BUFFER_SIZE: int = 32767 # max length for RAW socket (just in case, you know?)


def recv_buffered(sock: socket, length: int) -> bytes:
    result = b''
    left = length
    while left:
        new = sock.recv(min(left, BUFFER_SIZE))
        result += new
        left -= len(new)
    return result


def encode_packet(type: PacketType, payload: bytes) -> bytes:
    length = len(payload) + TYPE_LENGTH
    return (
        length.to_bytes(4, 'little', signed=False)
        + type.to_bytes(TYPE_LENGTH, 'little', signed=False)
        + payload
    )


def decode_packet(sock: socket) -> tuple[int, bytes]:
    length = int.from_bytes(sock.recv(sock, 4), 'little', signed=False)
    if length < 2:
        return (PacketType.INVALID_PACKET, b'')
    packet_type = PacketType.from_bytes(sock.recv(sock, 2))
    payload = recv_buffered(sock, length - 2)
    return packet_type, payload


def format_address(address) -> str:
    return f'[{address[0]}]:{address[1]}'
