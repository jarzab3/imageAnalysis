import cv2
import settings

log = settings.logging



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        log.debug("Init Camera")

    def __del__(self):
        self.video.release()


    def get_frame(self, color=True):
        self.video = cv2.VideoCapture(0)

        success, image = self.video.read()

        if not color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()