from flask import Flask, render_template, Response
import settings
from camera import VideoCamera

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

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    log.debug("Started up flask app")
    app.run(host='0.0.0.0', debug=True)