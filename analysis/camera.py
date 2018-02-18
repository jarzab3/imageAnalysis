import settings

log = settings.logging

import cv2
import numpy as np


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture()
        # self.video = cv2.VideoCapture('http://10.2.254.43:5000/video_feed')
        # frame = cv2.resize(frame, (640, 480))

        # self.cam = cv2.VideoCapture('http://100.72.197.92:5000/video_feed')

        # self.video.set(3, 640)
        # self.video.set(4, 480)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        log.info("Initialized video camera  ||| change")
        # self.video.open("http://localhost:5000/video_feed/")

        # cap = cv2.VideoCapture()
        # cap.open("http://169.254.197.26/")

    def __del__(self):
        pass
        # self.video.release()

    def url_to_image(self, url):
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        # resp = urllib.urlopen(url)


        response = urllib.request.urlopen(url)


        chunk = response.read(6 *1024)
        # response = requests.get(url, stream=True)
        # print (chunk)

        encode_param = [1, 90]

        image = np.asarray(bytearray(chunk), dtype="uint8")

        result, img = cv2.imencode('.jpg', image, encode_param)
        # image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # return the image
        print("opened url and returned image")
        # print (img)
        return img

    def cannyStream(self):
        success, frame = self.video.read()
        edges = cv2.Canny(frame, 200, 300)

    def get_frame(self, stream, color=True):
        bytes = ''

        while True:

            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                return image.tobytes()

        # if not color:
            # image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # return image



















    #
    # @staticmethod
    # def getImage():
    #     # stream = urllib.urlopen('http://localhost:5000/video_feed')
    #
    #     url = 'http://localhost:5000/video_feed'
    #
    #     with urllib.request.urlopen(url) as urlto:
    #         stream = urlto.read()
    #
    #     bytes = ''
    #     # while True:
    #     bytes += stream.read(1024)
    #     a = bytes.find('\xff\xd8')
    #     b = bytes.find('\xff\xd9')
    #
    #     i = None
    #
    #     if a != -1 and b != -1:
    #         jpg = bytes[a:b + 2]
    #         bytes = bytes[b + 2:]
    #         i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
    #
    #     return i
    #
    # def url_to_image(self, url):
    #     # download the image, convert it to a NumPy array, and then read
    #     # it into OpenCV format
    #     with urllib.request.urlopen(url) as urlto:
    #         resp = urlto.read()
    #
    #     print (resp)
    #     # resp = urllib.urlopen(url)
    #
    #     image = np.asarray(bytearray(resp.read()), dtype="uint8")
    #     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    #
    #     # return the image
    #     return image