from flask import Flask, render_template, Response, jsonify, request
import settings
from camera import VideoCamera
import time
import urllib2

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

log = settings.logging

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['TEMPLATES_AUTO_RELOAD'] = settings.TEMPLATES_AUTO_RELOAD


@app.route('/')
def index():
    return render_template('index.html')

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
    stream = urllib2.urlopen("http://100.72.197.92:5000/video_feed")
    bytes = ''
    import cv2
    import numpy as np

    while True:

        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n\r\n')

            time.sleep(0.00001)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, threaded=True)
    log.debug("Started up analysis app")

