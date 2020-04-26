import socket

import cv2
import libh264decoder
import numpy as np


def render_frame(frame):
    # convert color
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # display frame
    cv2.imshow("tello", image)
    cv2.waitKey(1)


def display_frame(decoded_frame):
    (frame, w, h, ls) = decoded_frame
    if frame is not None:
        # print(f"frame size {len(frame)} bytes, w {w}, h {h}, linesize {ls}")
        frame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
        frame = frame.reshape((h, ls // 3, 3))
        frame = frame[:, :w, :]
        render_frame(frame)


def decode_frames(decoder, frame_data):
    frames = decoder.decode(frame_data)
    for frame in frames:
        display_frame(frame)


print("Prepare sockets")
socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_cmd.bind(("0.0.0.0", 8889))
socket_video.bind(("0.0.0.0", 11111))

print("Initialize Tello")
tello_address = ("192.168.10.1", 8889)

socket_cmd.sendto("command".encode(), tello_address)
socket_cmd.sendto("streamon".encode(), tello_address)

print("Read video stream")
decoder = libh264decoder.H264Decoder()

frame_data = b""
while True:
    (data, address) = socket_video.recvfrom(2048)
    frame_data += data
    # end of frame
    if len(data) != 1460:
        decode_frames(decoder, frame_data)
        frame_data = b""

cv2.destroyAllWindows()
