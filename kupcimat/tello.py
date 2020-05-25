import logging
from socket import socket
from typing import Tuple


def tello_address() -> Tuple[str, int]:
    return "192.168.10.1", 8889


def send_cmd(cmd_socket: socket, command: str) -> str:
    logging.info("action=send-command command=%s", command)
    cmd_socket.sendto(command.encode(), tello_address())
    # TODO error handling and timeout
    response = None
    while response is None:
        response, address = cmd_socket.recvfrom(2048)
    return response.decode().strip()
