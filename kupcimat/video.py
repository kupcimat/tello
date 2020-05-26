import cv2
import cvlib as cv
import libh264decoder
import numpy as np

h264_decoder = libh264decoder.H264Decoder()


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
