import logging

from cop_server.server import Server


def main():
    logging.basicConfig(
        format='[%(asctime)s] [%(threadName)s/%(levelname)s] [%(filename)s:%(lineno)i]: %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )

    server = Server()
    server.listen()


main()
