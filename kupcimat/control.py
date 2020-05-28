import logging
import threading
from socket import socket

import time

import kupcimat.command as cmd
import kupcimat.tello as tello


class ControlThread(threading.Thread):
    def __init__(self, cmd_socket: socket):
        super().__init__(name="control-thread")
        self.socket = cmd_socket
        self.mid_points = []
        self.event = threading.Event()

    def run(self) -> None:
        logging.info("Initialize tello")
        tello.send_cmd(self.socket, cmd.command())
        tello.send_cmd(self.socket, cmd.stream_on())
        tello.send_cmd(self.socket, cmd.get_temperature())
        tello.send_cmd(self.socket, cmd.get_battery())
        while not self.event.is_set():
            logging.info("action=control points=%s", self.mid_points)
            tello.send_cmd(self.socket, cmd.get_battery())
            time.sleep(1)
        logging.info("action=control END")


def follow(x: int, y: int, x_target: int, y_target: int, diff: int) -> str:
    if abs(x - x_target) < diff:
        return cmd.command()
    if x < x_target:
        return cmd.left(20)
    else:
        return cmd.right(20)
