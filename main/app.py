from flask import Flask, render_template, Response, jsonify, request, redirect
from flask import send_file, send_from_directory
from flask_analytics import Analytics
from flask_basicauth import BasicAuth
from flask.views import View
import datetime

import settings
import time
import os
import urllib2
import numpy as np
import cv2
import imutils
import datetime
import base64
import subprocess
from OpenSSL import SSL
from flask_basicauth import BasicAuth
from Utils import *

# from camera import VideoCamera
from Utils import *

url = "http://visionstream.ngrok.io/stream.mjpg"

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

Analytics(app)

log = settings.logging

app.config['ANALYTICS']['GOOGLE_CLASSIC_ANALYTICS']['ACCOUNT'] = 'UA-115560866-1'

app.config['BASIC_AUTH_USERNAME'] = 'super'
app.config['BASIC_AUTH_PASSWORD'] = 'superpass'

basic_auth = BasicAuth(app)

# Define all routes
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/emotion')
def emotion():
    return render_template('emotion.html')

@app.route('/math')
def maths():
    return render_template('calculator.html')

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
# @basic_auth.required
def visionAnalysis():
    return render_template('visionAnalysis.html')

@app.route('/videoPlayer')
def play_video():
    return render_template('playVideo.html')

@app.route('/ai')
def artificialIntelligence():
    return render_template('artificialIntelligence.html')


@app.route('/aidocs')
def artificialIntelligenceDigitDocs():
    return render_template('documentation.html')


@app.route('/digitRecognition')
def artificialIntelligenceDigitRecognition():
    return render_template('drawDigit.html')

# Image analysis code below
# ------------------------------------------------------

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def playVideo(filename):
    uploads = os.path.join(app.root_path, "analysisOutput")
    return send_from_directory(directory=uploads, filename=filename, )

@app.route('/playVideo/<path:filename>', methods=['GET', 'POST'])
def downloadVideo(filename):
    uploads = os.path.join(app.root_path, "analysisOutput")
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

@app.route('/apiImage')
def ai_query_image():
    f = request.args.get('image')

    convert_and_save(f)

    log.info("Digit received from web. Start processing!")

    prediction = executeDigitRecognitionJava()

    log.info("Java executed. Predicted digit: {}".format(prediction))

    log.debug("Address: {}".format(request.remote_addr))

    return jsonify(result=prediction)

@app.route('/_apiQueryFileList')
def getFilesList():
    arg = request.args.get('apiQ0')

    log.info("Received request for filename on the server for 'analysisOutput' directory")

    arr = os.listdir('analysisOutput')

    return jsonify(result=arr)

color = True

@app.route('/_apiQueryColor')
def api_query_task():
    query = request.args.get('apiQ0', "", type=str).strip()

    # Add color var
    global color

    if query == "true":
        color = False
        reply = "Changed to gray scale"
    else:
        color = True
        reply = "Change to normal"

    return jsonify(result=reply)

backgroundSubtractorOn = False

@app.route('/_apiQueryBack')
def api_query_task1():

    query = request.args.get('apiQ0', "", type=str).strip()

    # add var
    global backgroundSubtractorOn

    if query == "true":
        backgroundSubtractorOn = True
        reply = "Changed to background extraction"

    else:
        backgroundSubtractorOn = False
        reply = "Change to normal"

    return jsonify(result=reply)

videoRecordingOn = False
@app.route('/_apiQueryRecord')
def api_query_task2():

    query = request.args.get('apiQ0', "", type=str).strip()

    # add var
    global videoRecordingOn

    if query == "true":
        videoRecordingOn = True
        reply = "Start recording"

    else:
        videoRecordingOn = False
        reply = "Stopped recorning"

    return jsonify(result=reply)

alpha = 0.5

@app.route('/_apiQueryBar')
def api_query_task_range_bar():
    query = request.args.get('apiQ0', "", type=float)
    global alpha
    alpha = query
    reply = "Adjusted alpha channel: {}".format(alpha)
    return jsonify(result=reply)


def identifyROI(frame):

    output = createBackgroundSubtractor(frame)

    _, contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # # loop over the contours
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 7000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (249, 255, 15), 2)

        print("Area is: {}".format(cv2.contourArea(c)))

        print (x, y, w, h)

    # return

def addGridLayer(frame):

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

    return output

# Background extraction inits
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

fgbg = cv2.createBackgroundSubtractorMOG2()

def createBackgroundSubtractor(frame):

    fgmask = fgbg.apply(frame)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    return fgmask

def initRecording(frame_width, frame_height):
        """
        This function initialises a frame recording and returns an object with video recording settings
        Define the codec and create VideoWriter object. The output is stored in 'analysisOutput/' directory as a filename video{date}avi
        :param frame_width:
        :param frame_height:
        :return: VideoWriter object
        """

        # Define the codec and create VideoWriter object. The output is stored in 'analysisOutput/' directory as a filename video{date}avi
        ts = datetime.datetime.now().strftime("_%A_%Y-%m-%d_%H:%M:%S")

        filename = "analysisOutput/video" + ts + ".avi"

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

        return [out, filename]


import os

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -loglevel panic -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True

def convertToGray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def detectMotion():
    stream = None

    try:
        stream = urllib2.urlopen(url)
        log.info("Successfully opened a stream")
    except urllib2.HTTPError as e:
        code = e.code
        log.error("URLLIB error while opening a stream: %s" % code)

    bytes = ''

    haveDetails = False

    frame_height = 480
    frame_width = 640

    global backgroundSubtractorOn
    global videoRecordingOn
    recordingInitialised = False
    recordingFilename = ""
    recordingFilenameNew = "Default"

    out = None

    if stream != None:
        while True:
            try:

                bytes += stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a != -1 and b != -1:
                    frameBytes = bytes[a:b + 2]
                    bytes = bytes[b + 2:]

                    nparr = np.fromstring(frameBytes, np.uint8)

                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    # Store details about frame only once
                    if not haveDetails:
                        # Get dimensions of the frames
                        frame_height, frame_width, frameChannels = frame.shape
                        haveDetails = True

                    # Video recording
                    if videoRecordingOn:

                        if not recordingInitialised:
                            recording = initRecording(frame_width, frame_height)
                            out = recording[0]
                            recordingFilename =  recording[1]
                            recordingFilenameNew = recordingFilename[:-4]
                            recordingInitialised = True
                            log.debug("Start recording a video.")

                        out.write(frame)

                    if not videoRecordingOn and recordingInitialised:
                        log.debug("Stop recording a video.")

                        if convert_avi_to_mp4(recordingFilename, recordingFilenameNew):
                            log.debug("File converted to mp4")

                            try:
                                os.remove(recordingFilename)
                                log.debug("Delete old avi file: %s" % recordingFilename)
                            except OSError:
                                pass

                        recordingInitialised = False

                    if backgroundSubtractorOn:

                        output = createBackgroundSubtractor(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    elif not color:
                        output = convertToGray(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    else:
                        output = addGridLayer(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    toSend = imageJPG.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + toSend + b'\r\n\r\n')

                    time.sleep(0.00001)

            except Exception as error:
                log.error("Error while streaming: %s" %error)

    else:
        log.debug("Closing connections")
        out.release()
        stream.close()


@app.route('/motion_detection')
def motion_detection():
    return Response(detectMotion(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem')
# context.use_certificate_file('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem')


if __name__ == '__main__':
    try:
        log.debug("Started up analysis app")
        # app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem','/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem'))
        app.run(host='0.0.0.0', port=80, threaded=True, debug=True)

        # while True: time.sleep(1)

    # except (KeyboardInterrupt, SystemExit):
    except Exception as error:
        log.debug("Error occurred while main execution %s" %error)
        # os.system('sudo lsof -t -i tcp:80 | xargs kill -9')
        # log.debug('Received keyboard interrupt, cleaning threads, closing closing connection on port 80')
