import logging
import socket

import kupcimat.control as control
import kupcimat.tello as tello
import kupcimat.video as video

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
control_thread = control.ControlThread(cmd_socket)
control_thread.start()

while True:
    frame = video_thread.frame
    if frame is not None:
        updated_frame, mid_points = video.detect_faces(frame)
        control_thread.mid_points = mid_points
        video.render_frame(updated_frame)
