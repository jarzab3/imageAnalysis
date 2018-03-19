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

    stream = urllib2.urlopen("http://127.0.0.1:5000/video_feed")
    bytes = ''

    while True:

        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            frameBytes = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            img = camera.makeImage(frameBytes, color, True)
            # image = camera.bytesToImage(frameBytes)

            # img = camera.findFaces(frameBytes)

            # canny = camera.changeToGray(image)

            # frameBytes = camera.imageToBytes(canny)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

            time.sleep(0.00001)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, threaded=True)
    log.debug("Started up analysis app")