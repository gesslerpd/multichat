import socket

from argparse import ArgumentParser
from ipaddress import IPv4Address
from contextlib import contextmanager

import trio

MAX_RECV = 65507


@contextmanager
def multicast_socket():
    sock = trio.socket.socket(
        trio.socket.AF_INET,
        trio.socket.SOCK_DGRAM
    )

    try:
        yield sock
    finally:
        sock.close()


async def sender(sock, group_address, port):
    while True:
        message = await trio.to_thread.run_sync(input)
        if message:
            await sock.sendto(message.encode(), (group_address, port))


async def receiver(sock):
    while True:
        data, (peer, _) = await sock.recvfrom(MAX_RECV)
        print(f'[{peer}] {data.decode()}')


async def _main(group_address, port, ttl):
    with multicast_socket() as sock:

        sock.setsockopt(
            trio.socket.IPPROTO_IP,
            trio.socket.IP_MULTICAST_TTL,
            ttl
        )

        membership = trio.socket.inet_aton(group_address) + bytes(4)
        sock.setsockopt(
            trio.socket.IPPROTO_IP,
            trio.socket.IP_ADD_MEMBERSHIP,
            membership
        )

        sock.setsockopt(
            trio.socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        await sock.bind(('', port))

        async with trio.open_nursery() as nursery:
            nursery.start_soon(receiver, sock)
            nursery.start_soon(sender, sock, group_address, port)


def main(args=None):
    parser = ArgumentParser(
        prog='multichat',
        description='Multicast chat client and server'
    )
    parser.add_argument(
        'group_address',
        help='multicast group address'
    )
    parser.add_argument(
        'port',
        help='port number',
        type=int
    )
    parser.add_argument(
        '--ttl',
        help='multicast time to live (default: 1)',
        type=int,
        default=1
    )
    args = parser.parse_args(args)

    group_address = str(IPv4Address(args.group_address))

    trio.run(_main, group_address, args.port, args.ttl)


if __name__ == '__main__':
    main()
