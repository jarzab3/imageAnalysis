from flask import Flask, render_template, Response, jsonify, request
import settings
# from camera import VideoCamera
import time
import urllib2

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

log = settings.logging

# def configure_app(flask_app):
#     flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
#     flask_app.config['TEMPLATES_AUTO_RELOAD'] = settings.TEMPLATES_AUTO_RELOAD


@app.route('/')
def index():
    return render_template('main.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
    log.debug("Started up analysis app")