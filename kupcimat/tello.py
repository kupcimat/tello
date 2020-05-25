import logging
import threading
from socket import socket
from typing import Tuple

import kupcimat.video as video


def tello_timeout() -> int:
    return 5


def tello_address() -> Tuple[str, int]:
    return "192.168.10.1", 8889


def send_cmd(cmd_socket: socket, command: str) -> None:
    logging.info("action=send-command command=%s", command)
    cmd_socket.sendto(command.encode(), tello_address())


class ReceiveCmdThread(threading.Thread):
    def __init__(self, cmd_socket: socket):
        super().__init__(name="cmd-thread", daemon=True)
        self.socket = cmd_socket
        self.response = None

    def run(self) -> None:
        while True:
            # TODO error handling
            (response, address) = self.socket.recvfrom(2048)
            self.response = response.decode().strip()
            logging.info("action=receive-response response=%s", self.response)


class ReceiveVideoThread(threading.Thread):
    def __init__(self, video_socket: socket):
        super().__init__(name="video-thread", daemon=True)
        self.socket = video_socket
        self.frame = None

    def run(self) -> None:
        packet_data = b""
        while True:
            (data, address) = self.socket.recvfrom(2048)
            packet_data += data
            if len(data) != 1460:  # end of frame
                for frame in video.decode_frames(packet_data):
                    self.frame = frame
                packet_data = b""
