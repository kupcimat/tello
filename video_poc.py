import socket
import threading

import cv2
import cvlib as cv
import libh264decoder
import numpy as np


def receive_video_stream():
    h264_decoder = libh264decoder.H264Decoder()
    packet_data = b""
    while True:
        (data, address) = socket_video.recvfrom(2048)
        packet_data += data
        # end of frame
        if len(data) != 1460:
            # TODO
            frames = decode_frames(h264_decoder, packet_data)
            global decoded_frame
            for frame in frames:
                decoded_frame = frame
            packet_data = b""


def decode_frames(decoder, packet_data):
    frames = []
    # decode and reshape data into frames
    for frame_data in decoder.decode(packet_data):
        (frame, w, h, ls) = frame_data
        if frame is not None:
            frame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
            frame = frame.reshape((h, ls // 3, 3))
            frame = frame[:, :w, :]
            frames.append(frame)
    return frames


def detect_faces(frame):
    (faces, confidences) = cv.detect_face(frame)
    # draw face rectangles
    for face in faces:
        start_point = (face[0], face[1])
        end_point = (face[2], face[3])
        cv2.rectangle(frame, start_point, end_point, color=(0, 255, 0), thickness=2)
    return frame


def render_frame(frame):
    # TODO can we skip using different reshape?
    # convert BGR to RBG colors
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("tello", rgb_frame)
    cv2.waitKey(1)


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
decoded_frame = None

threading.Thread(target=receive_video_stream, daemon=True).start()

while True:
    if decoded_frame is not None:
        render_frame(detect_faces(decoded_frame))
