from flask import Flask, render_template, Response, jsonify, request, redirect
from flask import send_file, send_from_directory
from flask_analytics import Analytics
from flask_basicauth import BasicAuth
from flask.views import View
import datetime
import pygal
import json
from pygal.style import DarkSolarizedStyle
from urllib2 import urlopen
import numpy
import thread
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
from scipy.spatial import distance
import sqlite3


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    alpha = float(query)
    reply = "Adjusted alpha channel: {}".format(alpha)
    return jsonify(result=reply)

# Database section
class DataManager:

    def __init__(self):

        self.mainDB = "databases/dataCollection"

    def createUpdateDatabase(self):
        """
        This function creates a new database.
        :return: n
        """
        create_table = '''CREATE TABLE IF NOT EXISTS main (id INTEGER PRIMARY KEY, created TEXT, week_day TEXT, hour TEXT, tracking_time TEXT, tag_id INTEGER )'''

        conn = sqlite3.connect(self.mainDB)

        db = conn.cursor()

        db.execute(create_table)

        log.debug("Successfully created db. %s" % self.mainDB)


    def saveToMainDB(self, data):

        db = sqlite3.connect(self.mainDB)

        try:
            with db:
                db.execute('''INSERT INTO main(created, week_day, hour, tracking_time, tag_id)
                          VALUES(?,?,?,?)''',
                           (data[0], data[1], data[2], data[3], data[4]))

        except sqlite3.Error as err:
            log.error("Error occurred: %s" % err)

        finally:
            log.debug("Successfully saved data to main db.")
            db.close()

    def retriveDataFromDB(self, dayWeek):
        """
        This method search for urls for selected dayWeek name
        :param dayWeek:
        :return: array - data
        """
        conn = sqlite3.connect(self.mainDB)

        cursor = conn.cursor()

        cursor.execute('''SELECT urls FROM main WHERE week_day=?''', (dayWeek,))

        data = cursor.fetchone()

        log.debug("Successfully read urls form DB")

        return data

@app.route('/visualisation')
def displayData():
    graph = pygal.Line()
    # graph.title = 'Pedestrians data'

    graph.x_labels = ['06:00', '07:00', '08:00', '09:00', '10:00', '12:00', '13:00', '14:00', '15:00',
                      '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']

    a = numpy.random.random_integers(0, 20, 16)
    a1 = numpy.random.random_integers(0, 30, 16)
    a2 = numpy.random.random_integers(0, 20, 16)
    a3 = numpy.random.random_integers(0, 25, 16)
    a4 = numpy.random.random_integers(0, 30, 16)
    a5 = numpy.random.random_integers(0, 15, 16)
    a6 = numpy.random.random_integers(0, 31, 16)

    graph.add('Monday', a)
    graph.add('Tuesday', a1)
    graph.add('Wednesday', a2)
    graph.add('Thursday', a3)
    graph.add('Friday', a4)
    graph.add('Saturday', a5)
    graph.add('Sunday', a6)

    graph_data = graph.render_data_uri()

    return render_template('graphs.html', graph_data = graph_data)


def identifyROI(frame):

    output = createBackgroundSubtractor(frame)

    _, contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boundingRect = False
    (x, y, w, h) = (0,0,0,0)

    cX = None
    cY = None
    # # loop over the contours
    for c in contours:
        # if cv2.contourArea(c) > 00:
        # print("1) Area is: {}".format(cv2.contourArea(c)))

        # if the contour is too small, ignore it
        if cv2.contourArea(c) > 500 and cv2.contourArea(c) < 300000:

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            boundingRect = True

            areaOfObject = cv2.contourArea(c)


            M = cv2.moments(c)
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])

            cv2.circle(frame, (cX, cY), 2, (0, 0, 255), -1)

            if False:

                cv2.putText(frame, str(areaOfObject), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.50,
                            (255, 0, 255), 1)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (249, 255, 15), 2)

            # print ("cx: {} cy: {}".format(cX, cY))

            # print("Found object of interest position: {}, area is: {}".format((x, y, w, h), areaOfObject))

    return [frame, boundingRect, (x, y, w, h), [cX, cY]]


def addGridLayer(frame):

    # Get dimensions of the frames
    height, width, channels = frame.shape

    # Add overlay layer for different opacity
    overlay = frame.copy()

    global alpha

    output = frame.copy()

    color = (214, 178, 118)

    offset = 3 + 9

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

    fgmask = cv2.GaussianBlur(fgmask, (5, 5), 0)

    fgmask = cv2.medianBlur(fgmask, 5)

    fgmask = cv2.bilateralFilter(fgmask, 9, 75, 75)

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
    log.debug("File converted to mp4")
    try:
        os.remove(avi_file_path)
        log.debug("Delete old avi file: %s" % avi_file_path)
    except OSError:
        pass


def convertToGray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


(major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

class Tracker:

    def __init__(self, bbox, frame, tagName):
        self.bbox = bbox
        self.tagName = tagName

        self.time_on = time.time()
        self.time_off = 0

        self.center = (int(self.bbox[0] + (self.bbox[2] / 2)), int(self.bbox[1] + (self.bbox[3] / 2)))

        self.tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
        self.tracker_type = self.tracker_types[2]

        if int(minor_ver) < 3:
            self.tracker = cv2.Tracker_create(self.tracker_type)
        else:
            if self.tracker_type == 'BOOSTING':
                self.tracker = cv2.TrackerBoosting_create()
            if self.tracker_type == 'MIL':
                self.tracker = cv2.TrackerMIL_create()
            if self.tracker_type == 'KCF':
                self.tracker = cv2.TrackerKCF_create()
            if self.tracker_type == 'TLD':
                self.tracker = cv2.TrackerTLD_create()
            if self.tracker_type == 'MEDIANFLOW':
                self.tracker = cv2.TrackerMedianFlow_create()
            if self.tracker_type == 'GOTURN':
                self.tracker = cv2.TrackerGOTURN_create()

        self.ok = self.tracker.init(frame, self.bbox)
        self.refObj = None

    def checkForNewToAdd(self, point):
        dst = distance.euclidean(point, self.center)
        return dst

    def updateTracking(self, frame):

        # Start timer
        timer = cv2.getTickCount()

        self.ok, self.bbox = self.tracker.update(frame)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bound9ing box
        if self.ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))

            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            # Update center of tracking point
            self.center = (int(self.bbox[0] + (self.bbox[2] / 2)), int(self.bbox[1] + (self.bbox[3] / 2)))

            # Draw tag name above the person
            cv2.putText(frame,  str(self.tagName), (p1[0], p1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (255, 255, 0), 1)

            # print ("Box: {} x: {}, y: {}".format(self.bbox, self.bbox[]))

            # Draw center of the tracker
            cv2.circle(frame, self.center, 2, (0, 0, 255), -1)

        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (50, 170, 50), 2)

        # Display FPS on frame
        # cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
        #             (50, 170, 50), 2)
        #
        return [frame, self.ok]


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

    lookingForROI = True

    trackFailureReported = False

    tagName = 0

    trackers = []
    # Distance where new tracker can be enabled
    newTrackerThreshold = 150

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
                            # bbox = (287, 23, 86, 320)
                            # t = Tracker(bbox, output, tagName)
                            # trackers.append(t)
                            # tagName += 1

                        if lookingForROI:

                            # Change it after testing
                            roi = identifyROI(frame)

                            output = roi[0]
                            foundROI = roi[1]
                            newROI = roi[3]
                            bbox = roi[2]


                        if foundROI != False and len(trackers) == 0:
                            # lookingForROI = False

                            # Attach to a tracker and create an object
                            tracker_time = time.time()
                            t = Tracker(bbox, output, tagName)
                            trackerInstance = [t, tracker_time, True, trackFailureReported]

                            trackers.append(trackerInstance)

                            tagName += 1

                            # t = Tracker(bbox, output, tagName)

                            # trackers.append(t)
                            # tagName += 1

                            trackingStarted = True

                            # lookingForROI = False

                        if trackingStarted:

                            # Random number above the newTrackerThreshold
                            smallestDistance = 1000

                            for index, tracker in enumerate(trackers):
                                trackerResults = tracker[0].updateTracking(output)

                                output = trackerResults[0]
                                is_ok = trackerResults[1]

                                # print (len(trackers), newROI)

                                # Check if distance between all trackers and new object is big enough and if is then add this object to tracking.
                                if newROI[0]  != None and newROI[1] !=None:
                                    if len(trackers) == 0:
                                        # print ("add new tracker")
                                        tracker_time = time.time()
                                        t = Tracker(bbox, output, tagName)
                                        trackerInstance = [t, tracker_time, True, trackFailureReported]

                                        trackers.append(trackerInstance)

                                        tagName +=1


                                    if tracker[0].checkForNewToAdd(newROI) < smallestDistance:
                                        smallestDistance = tracker[0].checkForNewToAdd(newROI)
                                        # print (smallestDistance)


                                # Update if is a successful tracker
                                tracker[2] = is_ok

                                if tracker[2] and is_ok:
                                    # print ("ok Tracker: {} time on: {}\n".format(tracker[0].tagName, time.time() - tracker[1]))
                                    pass

                                elif not tracker[2] and not is_ok and not tracker[3]:
                                    log.info("Track failure reported for tracker: {}".format(tracker[0].tagName))
                                    tracker_time = time.time()
                                    tracker[1] = tracker_time
                                    tracker[3] = True

                                if tracker[3] and (time.time() - tracker[1]) >= 3:
                                    del trackers[index]
                                    log.info("Tracker deleted {}".format(tracker[0].tagName))



                                if tracker[2] and not tracker[3]:
                                    tracker[3] = False
                                    tracker[1] = time.time()

                                #     print (" not ok Tracker: {} time on: {}\n".format(tracker[0].tagName, time.time() - tracker[1]))


                            # Update time for tracker if positive carry on, if negative for more than threshold then delete
                            if smallestDistance > newTrackerThreshold and smallestDistance != 1000:

                                log.info("Dist between current tracker and new found ROI. {} . Add new tracker".format(smallestDistance))

                                tracker_time = time.time()
                                t = Tracker(bbox, output, tagName)
                                trackerInstance = [t, tracker_time, True, trackFailureReported]

                                trackers.append(trackerInstance)

                                tagName += 1



                            # lastFound = datetime.datetime.now()
                            # if (timestamp - lastUploaded).seconds >= 3.0:
                            # timestamp = datetime.datetime.now()

                        # if not trackingStarted:

                        ret, imageJPG = cv2.imencode('.jpg', output)

                    elif not trackingOn and trackingInitialised:
                        log.debug("Tracking disabled")
                        trackingInitialised = False
                        trackingStarted = False

                        trackers = []
                        # In order to keep looking comment it out
                        # lookingForROI = True

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

                        # Create start_new_thread thread
                        try:
                            thread.start_new_thread(convert_avi_to_mp4, (recordingFilename, recordingFilenameNew,))
                        except Exception as error:
                            log.error("Error: unable to start 'convert_avi_to_mp4' thread. %s" %error)

                        recordingInitialised = False

                    # Convert to jpeg and stream to template
                    toSend = imageJPG.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + toSend + b'\r\n\r\n')


                    time.sleep(0.00001)

            except IOError as e:
                log.error("IO Error while streaming: %s" % error)

            except Exception as error:
                log.error("Error while streaming: %s" % error)

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
