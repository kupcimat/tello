import logging
import threading
from socket import socket

import time

import kupcimat.command as cmd
import kupcimat.tello as tello


class ControlThread(threading.Thread):
    def __init__(self, cmd_socket: socket):
        super().__init__(name="control-thread", daemon=True)
        self.socket = cmd_socket
        self.mid_points = []

    def run(self) -> None:
        logging.info("Initialize tello")
        tello.send_cmd(self.socket, cmd.command())
        tello.send_cmd(self.socket, cmd.stream_on())
        tello.send_cmd(self.socket, cmd.get_temperature())
        tello.send_cmd(self.socket, cmd.get_battery())
        while True:
            logging.info("action=control points=%s", self.mid_points)
            time.sleep(1)
