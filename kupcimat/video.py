import cv2
import cvlib as cv
import libh264decoder
import numpy as np

import kupcimat.util as util

h264_decoder = libh264decoder.H264Decoder()


# TODO add types
def decode_frames(packet_data):
    frames = []
    # decode and reshape data into frames
    for frame_data in h264_decoder.decode(packet_data):
        (frame, w, h, ls) = frame_data
        if frame is not None:
            frame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
            frame = frame.reshape((h, ls // 3, 3))
            frame = frame[:, :w, :]
            frames.append(frame)
    return frames


def detect_faces(frame):
    mid_points = []
    (faces, confidences) = cv.detect_face(frame)
    # draw face rectangles
    for face in faces:
        (x1, y1, x2, y2) = face
        mid_points.append(util.find_mid_point(x1, y1, x2, y2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
    return frame, mid_points


def render_frame(frame):
    # TODO can we skip using different reshape?
    # convert BGR to RBG colors
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("tello", rgb_frame)
    cv2.waitKey(1)
