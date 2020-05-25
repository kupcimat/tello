import logging
import socket

import kupcimat.tello as tello

logging.basicConfig(level=logging.DEBUG)

logging.info("Initialize sockets")
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd_socket.bind(("0.0.0.0", 8889))

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind(("0.0.0.0", 11111))

logging.info("Initialize tello")
logging.info(tello.send_cmd(cmd_socket, "command"))
logging.info(tello.send_cmd(cmd_socket, "streamon"))

logging.info(tello.send_cmd(cmd_socket, "temp?"))
logging.info(tello.send_cmd(cmd_socket, "battery?"))
