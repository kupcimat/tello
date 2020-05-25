import logging
import socket

import time

import kupcimat.command as cmd
import kupcimat.tello as tello

logging.basicConfig(level=logging.DEBUG)

logging.info("Initialize sockets")
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd_socket.bind(("0.0.0.0", 8889))
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind(("0.0.0.0", 11111))

logging.info("Initialize threads")
cmd_thread = tello.ReceiveCmdThread(cmd_socket)
cmd_thread.start()
video_thread = tello.ReceiveVideoThread(video_socket)
video_thread.start()

logging.info("Initialize tello")
tello.send_cmd(cmd_socket, cmd.command())
tello.send_cmd(cmd_socket, cmd.stream_on())

tello.send_cmd(cmd_socket, cmd.get_temperature())
tello.send_cmd(cmd_socket, cmd.get_battery())

time.sleep(10)
