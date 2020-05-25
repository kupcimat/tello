import logging
import socket

import kupcimat.command as cmd
import kupcimat.tello as tello

logging.basicConfig(level=logging.DEBUG)

logging.info("Initialize sockets")
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd_socket.bind(("0.0.0.0", 8889))

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind(("0.0.0.0", 11111))

logging.info("Initialize tello")
logging.info(tello.send_cmd(cmd_socket, cmd.command()))
logging.info(tello.send_cmd(cmd_socket, cmd.stream_on()))

logging.info(tello.send_cmd(cmd_socket, cmd.get_temperature()))
logging.info(tello.send_cmd(cmd_socket, cmd.get_battery()))
