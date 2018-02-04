import cv2
from settings import logging

import gevent.monkey

gevent.monkey.patch_all()

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)

        # frame = cv2.resize(frame, (640, 480))

        self.video.set(3, 640)
        self.video.set(4, 480)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        logging.info("Initialized video camera")

    def __del__(self):
        self.video.release()

    def cannyStream(self):
        success, frame = self.video.read()

        edges = cv2.Canny(frame, 200, 300)

    def get_frame(self, color=True):

        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if not color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()