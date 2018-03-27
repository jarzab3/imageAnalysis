from flask import Flask, render_template, Response, jsonify, request
import settings
from camera import VideoCamera
import time
import urllib2
import numpy as np
import cv2
import imutils
import datetime
import base64
import subprocess
from flask import send_file, send_from_directory
from flask_analytics import Analytics
from OpenSSL import SSL


url = "http://visionstream.ngrok.io/stream.mjpg"

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

Analytics(app)

log = settings.logging

app.config['ANALYTICS']['GOOGLE_CLASSIC_ANALYTICS']['ACCOUNT'] = 'UA-115560866-1'


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/emotion')
def emotion():
    return render_template('emotion.html')


# For AI pages
@app.route('/getDataSet1')
def getDataSet1():
    return render_template('cw2DataSet1.csv')


@app.route('/getDataSet2')
def getDataSet2():
    return render_template('cw2DataSet2.csv')


# Download example. It is
@app.route('/getDataSet2turnedoff')  # this is a job for GET, not POST
def plot_csv1():
    return send_file('extraFiles/cw2DataSet2.csv',
                     mimetype='text/csv',
                     attachment_filename='cw2DataSet2.csv',
                     as_attachment=True)


@app.route('/viewCV')
def view_resume():
    return render_template('pdfViewer.html')

@app.route('/downloadCV')
def download_resume():
    return send_file('static/other/adam_jarzebak_cv.pdf', mimetype='pdf', as_attachment=True)


def convert_and_save(b64_string):
    str1 = b64_string[22:]

    data = base64.b64decode(str1)

    fileWriter = open("digit/digit.png", "wb")
    fileWriter.write(data)
    fileWriter.close()


def executeDigitRecognitionJava():
    try:
        response = subprocess.check_output("java Main", shell=True, stderr=subprocess.STDOUT, cwd="digit/")
        return response
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        #     return "Error while trying to recognize digit. Please try later."


@app.route('/vision')
def visionAnalysis():
    return render_template('visionAnalysis.html')


@app.route('/ai')
def artificialIntelligence():
    return render_template('artificialIntelligence.html')


@app.route('/aidocs')
def artificialIntelligenceDigitDocs():
    return render_template('documentation.html')


@app.route('/digitRecognition')
def artificialIntelligenceDigitRecognition():
    return render_template('drawDigit.html')


@app.route('/apiImage')
def ai_query_image():
    f = request.args.get('image')

    convert_and_save(f)

    log.info("Digit received from web. Start processing!")

    prediction = executeDigitRecognitionJava()

    log.info("Java executed. Predicted digit: {}".format(prediction))

    log.debug("Address: {}".format(request.remote_addr))

    return jsonify(result=prediction)



# TODO fix global var

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

alpha = 0.5

@app.route('/_apiQueryBar')
def api_query_task_range_bar():
    query = request.args.get('apiQ0', "", type=float)
    global alpha

    alpha = query

    reply = "Adjusted alpha channel: {}".format(alpha)

    print (reply)

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
        log.error("URLLIB eror: %s" % code)

    bytes = ''

    firstFrame = None

    global alpha


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

                # Get dimensions of the frames
                height, width, channels = frame.shape


                # Add ovrlay layer for different opacity
                overlay = frame.copy()

                output = frame.copy()

                color = (214, 178, 118)

                meters = 10

                for hei in np.arange(height, 0, -80):
                    cv2.putText(overlay, str(meters),
                                (10, hei - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                    cv2.line(overlay, (0, hei), (width, hei), color, 1)

                    meters += 5

                # apply the overlay
                cv2.addWeighted(overlay, alpha, output, 1 - alpha,
                                0, output)


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
                # cv2.putText(frame, "Status: {}".format(text), (10, 20),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                #             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)



                # ret, imageJPG = cv2.imencode('.jpg', frame)

                ret, imageJPG = cv2.imencode('.jpg', output)

                toSend = imageJPG.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + toSend + b'\r\n\r\n')

                time.sleep(0.00001)

    else:
        pass


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/motion_detection')
def motion_detection():
    return Response(detectMotion(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem')
# context.use_certificate_file('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem','/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem'))
    app.run(host='0.0.0.0', port=80, threaded=True, debug=False)
    log.debug("Started up analysis app")
