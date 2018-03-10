from flask import Flask, render_template, Response, jsonify, request
import settings
from camera import VideoCamera
import time
import urllib2
import numpy as np
import cv2
import imutils
import datetime
from flask import send_file

url = "http://d40ed2d7.ngrok.io/stream.mjpg"

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

log = settings.logging

@app.route('/')
def index():
    return render_template('main.html')

# For AI pages
@app.route('/getDataSet1')
def getDataSet1():
    return render_template('cw2DataSet1.csv')

@app.route('/getDataSet2')
def getDataSet2():
    return render_template('cw2DataSet2.csv')

# Download example. It is
@app.route('/getDataSet2turnedoff') # this is a job for GET, not POST
def plot_csv1():
    return send_file('extraFiles/cw2DataSet2.csv',
                     mimetype='text/csv',
                     attachment_filename='cw2DataSet2.csv',
                     as_attachment=True)

@app.route('/vision')
def visionAnalysis():
    return render_template('visionAnalysis.html')


@app.route('/ai')
def artificialIntelligence():
    return render_template('artificialIntelligence.html')

@app.route('/google55373b07f5339c7e.html')
def google():
    return render_template('google55373b07f5339c7e.html')


color = True

@app.route('/_apiQuery')
def api_query_task():

    query = request.args.get('apiQ0', "", type=str).strip()
    global color

    reply = ""

    if query == "color":
        color = True
        reply = "Changed to color"
    elif query == "gray":
        color = False
        reply = "Changed to gray"

    return jsonify(result=reply)

def gen(camera):

    stream = urllib2.urlopen("http://68958932.ngrok.io/stream.mjpg")
    bytes = ''

    while True:

        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            frameBytes = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            img = camera.makeImage(frameBytes, color, False)
            # image = camera.bytesToImage(frameBytes)

            # img = camera.findFaces(frameBytes)

            # canny = camera.changeToGray(image)

            # frameBytes = camera.imageToBytes(canny)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

            time.sleep(0.00001)


def detectMotion():
    stream = None

    try:
        stream = urllib2.urlopen(url)
        log.info("Successfully opened stream")
    except urllib2.HTTPError as e:
        code = e.code
        log.error("URLLIB eror: %s" %code)

    bytes = ''

    firstFrame = None

    if stream != None:
        while True:

            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                frameBytes = bytes[a:b + 2]
                bytes = bytes[b + 2:]

                nparr = np.fromstring(frameBytes, np.uint8)

                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


                # grab the current frame and initialize the occupied/unoccupied
                # text
                # (grabbed, frame) = camera.read()
                text = "Unoccupied"
                #
                # # if the frame could not be grabbed, then we have reached the end
                # # of the video
                #
                # if not grabbed:
                #     break

                # # resize the frame, convert it to grayscale, and blur it
                # frame = imutils.resize(frame, width=500)
                frame = cv2.resize(frame, (640, 480))

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                #
                # # if the first frame is None, initialize it
                if firstFrame is None:
                    firstFrame = gray
                    continue

                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                # dilate the thresholded image to fill in holes, then find contours
                # on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                (cnts, _, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_SIMPLE)

                # loop over the contours
                for c in cnts:
                    # if the contour is too small, ignore it
                    # print(len(cnts))
                    pass

                    # print (cv2.contourArea(c))
                    # if cv2.contourArea(c) < args["min_area"]:
                    #     continue

                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    # (x, y, w, h) = cv2.boundingRect(c)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # text = "Occupied"

                # draw the text and timestamp on the frame
                cv2.putText(frame, "Status: {}".format(text), (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


                ret, imageJPG = cv2.imencode('.jpg', frame)


                toSend = imageJPG.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + toSend + b'\r\n\r\n')

                time.sleep(0.00001)

    else:
        pass

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')\


@app.route('/motion_detection')
def motion_detection():
    return Response(detectMotion(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
    log.debug("Started up analysis app")