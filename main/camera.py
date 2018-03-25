import settings
import cv2
import numpy as np

log = settings.logging

class VideoCamera(object):
    def __init__(self):
        log.info("Initialized video camera")

    def __del__(self):
        pass
        # self.video.release()

    def cannyStream(self, frame):
        edges = cv2.Canny(frame, 200, 300)

        return edges


    def bytesToImage(self, bytes, color=False):

        nparr = np.fromstring(bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if not color:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, image = cv2.imencode('.jpg', img)

        return image


    def findFaces(self, bytes):

        nparr = np.fromstring(bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        ret, frame = cv2.imencode('.jpg', img)

        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # print (len(faces))
        if (len(faces) > 0):
            print("Found: {}".format(len(faces)))
        else:
            print("Not found:")
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame


    def makeImage(self, bytes, color=True, backSub=False):
        nparr = np.fromstring(bytes, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if backSub:
            fgbg = cv2.createBackgroundSubtractorMOG2()
            image = fgbg.apply(image)

            ret, jpeg = cv2.imencode('.jpg', image)

            return jpeg.tobytes()


        if not color:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            ret, jpeg = cv2.imencode('.jpg', gray)

            return jpeg.tobytes()

        else:
            ret, jpeg = cv2.imencode('.jpg', image)

            return jpeg.tobytes()


    def imageToBytes(self, image):

        return image.tobytes()