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

url = "http://visionstream.eu.ngrok.io/stream.mjpg"
# url = "rtsp://visionstream.eu.ngrok.io/stream"

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

@app.route('/playVideo/<path:filename>', methods=['GET', 'POST'])
def playVideo(filename):
    uploads = os.path.join(app.root_path, "analysisOutput")
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def downloadVideo(filename):
    uploads = os.path.join(app.root_path, "analysisOutput")
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

@app.route('/play')
def playVideo_new():
    # uploads = os.path.join(app.root_path, "analysisOutput")
    return render_template('playVideo.html')

    # return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

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

    listOfFiles = os.listdir('analysisOutput')

    listOfFilesFiltered = []

    # Filter files, and return only with extension of '.mp4'
    for fil in listOfFiles:
        if fil[-4:] == ".mp4":
            listOfFilesFiltered.append(fil)

    return jsonify(result=listOfFilesFiltered)

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


trackingOn = False

@app.route('/_apiQueryTracking')
def api_query_task3():

    query = request.args.get('apiQ0', "", type=str).strip()

    # add var
    global trackingOn

    if query == "true":
        trackingOn = True
        reply = "Tracking enabled"

    else:
        trackingOn = False
        reply = "Disable tracking"

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

    boundingRect = False
    (x, y, w, h) = (0,0,0,0)
    # bbox = (287, 23, 86, 320)


    # # loop over the contours
    for c in contours:
        # if cv2.contourArea(c) > 00:
        #     print("1) Area is: {}".format(cv2.contourArea(c)))

        # if the contour is too small, ignore it
        if cv2.contourArea(c) > 200 and cv2.contourArea(c) < 300000:

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            boundingRect = True

            cv2.rectangle(frame, (x, y), (x + w, y + h), (249, 255, 15), 2)

            areaOfObject = cv2.contourArea(c)

            # print("Area is: {}".format(areaOfObject))

        # print (x, y, w, h)

    return [frame, boundingRect, (x, y, w, h)]


def addGridLayer(frame):

    # Get dimensions of the frames
    height, width, channels = frame.shape

    # Add overlay layer for different opacity
    overlay = frame.copy()

    output = frame.copy()

    color = (214, 178, 118)

    offset = 3

    distanceValues= [0 + offset, 4 + offset, 7 + offset, 13 + offset, 16 + offset]

    for hei in distanceValues:
        height -= 2

        cv2.putText(overlay, str(hei),
                    (10, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.line(overlay, (0, height), (width, height), color, 1)

        height -= 80

    # apply the overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha,
                    0, output)

    return output

# Background extraction init
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
        ts = datetime.datetime.now().strftime("_%Y-%m-%d_%H:%M:%S_%A")

        filename = "analysisOutput/video" + ts + ".avi"

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        out = cv2.VideoWriter(filename, fourcc, 25.0, (frame_width, frame_height))

        return [out, filename]

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -loglevel panic -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True

def convertToGray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


(major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')


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
    global trackingOn

    recordingInitialised = False
    trackingInitialised = False
    trackingStarted = False
    recordingFilename = ""
    recordingFilenameNew = "Default"

    out = None

    # Set up tracker.
    # Instead of MIL, you can also use
    # (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()

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

                    # Init default outputs
                    output = frame
                    imageJPG = frame

                    # Store details about frame only once
                    if not haveDetails:
                        # Get dimensions of the frames
                        frame_height, frame_width, frameChannels = frame.shape
                        haveDetails = True

                    if backgroundSubtractorOn:

                        output = createBackgroundSubtractor(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    elif not color:
                        output = convertToGray(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    elif trackingOn:

                        if not trackingInitialised:
                            log.debug("Tracking enabled")
                            trackingInitialised = True

                        # bbox = []

                        # Add layer of grid
                        # frame = addGridLayer(frame)

                        # Change it after testing
                        roi = identifyROI(frame)

                        output = roi[0]

                        bbox = (0, 0, 0, 0)

                        if roi[1] != False and not trackingStarted:
                            bbox = roi[2]

                            bbox1 = (287, 23, 86, 320)

                            # lastFound = datetime.datetime.now()
                            # if (timestamp - lastUploaded).seconds >= 3.0:
                            # timestamp = datetime.datetime.now()

                            log.info("Area of ROI: {}. Initialised tracker".format(bbox))

                            # trackerInit = initTracker()

                            # tracker =  trackerInit[0]

                            # tracker_type = tracker[1]

                            ok = tracker.init(frame, bbox)

                            trackingStarted = True

                        if trackingStarted:
                            # Start timer
                            timer = cv2.getTickCount()

                            ok, bbox = tracker.update(output)

                            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

                            # Draw bounding box
                            if ok:

                                # Tracking success
                                p1 = (int(bbox[0]), int(bbox[1]))
                                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                                cv2.rectangle(output, p1, p2, (255, 0, 0), 2, 1)
                            else:

                                # Tracking failure
                                cv2.putText(output, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                            (0, 0, 255), 2)

                            # Display tracker type on frame
                            cv2.putText(output, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                        (50, 170, 50), 2)

                            # Display FPS on frame
                            cv2.putText(output, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                        (50, 170, 50), 2)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    elif not trackingOn and trackingInitialised:
                        log.debug("Tracking disabled")
                        trackingInitialised = False
                        trackingStarted = False

                        output = addGridLayer(frame)
                        ret, imageJPG = cv2.imencode('.jpg', output)

                    else:
                        output = addGridLayer(frame)

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    # Video recording
                    if videoRecordingOn:

                        if not recordingInitialised:
                            recording = initRecording(frame_width, frame_height)
                            out = recording[0]
                            recordingFilename =  recording[1]
                            recordingFilenameNew = recordingFilename[:-4]
                            recordingInitialised = True
                            log.debug("Start recording a video.")

                        out.write(output)

                    if not videoRecordingOn and recordingInitialised:
                        log.debug("Stop recording a video.")
                        out.release()

                        if convert_avi_to_mp4(recordingFilename, recordingFilenameNew):
                            log.debug("File converted to mp4")

                            try:
                                os.remove(recordingFilename)
                                log.debug("Delete old avi file: %s" % recordingFilename)
                            except OSError:
                                pass

                        recordingInitialised = False

                    # Convert to jpeg and stream to template
                    toSend = imageJPG.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + toSend + b'\r\n\r\n')


                    time.sleep(0.00001)

            except IOError as e:
                # if e.errno == errno.EPIPE:
                log.error("IO Error while streaming: %s" % error)
            # except Exception as error:
            #     log.error("Error while streaming: %s" %error)

    else:
        pass
        # log.debug("Closing connections")
        # stream.close()


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
