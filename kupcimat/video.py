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
