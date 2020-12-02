from logging import StreamHandler
import socket
import select
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(StreamHandler(sys.stdout))

if __name__ == "__main__":
    #  TODO Connection information should be given via script arguments
    server_ip = '93.158.238.18'
    server_port = 30019
    client_bind_port = 30000

    logger.info(f"Starting proxy to {server_ip}")

    # Wait for the game client to connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(('0.0.0.0', client_bind_port))
    client_socket.listen(0)
    client, addr = client_socket.accept()
    logger.info(f"Client connected.")

    # When a client is connected, we open a connection to the target server
    logger.info(f"Connect to server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_ip, server_port))
    logger.info(f"Connected to server.")

    while True:
        try:
            # https://docs.python.org/3/library/select.html#select.select
            ready_to_read, _, _ = select.select([client, server], [], [], 0)
            for connection in ready_to_read:
                try:
                    # Prevent timeout exceptions by using the MSG_DONTWAIT flag
                    # https://manpages.debian.org/buster/manpages-dev/recv.2.en.html#The_flags_argument
                    data = connection.recv(4096 * 8, socket.MSG_DONTWAIT)

                    if connection.getsockname()[1] == client_bind_port:
                        # data came from the client
                        server.send(data)
                    else:
                        # data came from the server
                        client.send(data)
                except Exception as e:
                    logger.error("Connection problem", e)

        except KeyboardInterrupt as e:
            logger.info('Proxy terminated by user')
            break