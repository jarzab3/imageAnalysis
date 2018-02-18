from flask import Flask, render_template, Response, jsonify, request
import settings
from cameraStream import VideoCamera
import time

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
    return render_template('stream.html')

# color = True

# capture.open("http://127.0.0.1:5555/#droneStream");
#
# @app.route('/_apiQuery')
# def api_query_task():
#
#     query = request.args.get('apiQ0', "", type=str).strip()
#     global color
#
#     reply = ""
#
#     if query == "color":
#         color = True
#         reply = "Changed to color"
#     elif query == "gray":
#         color = False
#         reply = "Changed to gray"
#
#     return jsonify(result=reply)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        time.sleep(0.00001)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    log.debug("Started up streaming video")

