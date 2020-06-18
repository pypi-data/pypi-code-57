from flask import Flask
from flask_socketio import SocketIO
from flask import send_from_directory
from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.protocol import Note
import zumidashboard.scripts as scripts
import zumidashboard.sounds as sound
import zumidashboard.updater as updater
from zumidashboard.drive_mode import DriveMode
import time, subprocess, os, re, base64
from threading import Thread
import logging
from logging.handlers import RotatingFileHandler

from threading import Thread

if not os.path.isdir('/home/pi/Dashboard/debug'):
    os.mkdir('/home/pi/Dashboard/debug')

app = Flask(__name__, static_url_path="", static_folder='dashboard')
app.zumi = Zumi()
app.screen = Screen(clear=False)
app.action = ''
app.action_payload = ''
socketio = SocketIO(app)
usr_dir = '/home/pi/Dashboard/user/'
handler = RotatingFileHandler('/home/pi/Dashboard/debug/dashboard.log', maxBytes=10000, backupCount=1)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
lib_dir = os.path.dirname(os.path.abspath(__file__))
app.drive_mode = DriveMode(app.zumi)
app.drive_thread = ''


def _awake():
    app.screen.hello()
    sound.wake_up_sound(app.zumi)


def log(msge):
    app.logger.info(time.strftime('{%Y-%m-%d %H:%M:%S} ') + msge)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# network connect -------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')


@socketio.on('disconnect')
def test_disconnect():
    print('Socket disconnected')
    log('client disconnected')


@socketio.on('connect')
def test_connect():
    print('a client is connected')
    log('a client is connected')
    log(app.action)
    if app.action == 'check_internet' or app.action == 'check_last_network':
        time.sleep(1)
        socketio.emit(app.action, app.action_payload)
        app.action = ''
        app.action_payload = ''


@socketio.on('kill_supplicant')
def kill_supplicant():
    scripts.kill_supplicant()


@socketio.on('check_camera_connection')
def check_camera_connection():
    from zumi.util.camera import Camera
    try:
        camera = Camera(auto_start=True)
        frame = camera.capture()
        camera.close()
        socketio.emit('check_camera_connection', True)
    except:
        socketio.emit('check_camera_connection', False)


@socketio.on('check_drive_server')
def check_drive_server():
    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '3456'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        print('drive server is not ready')
        socketio.emit('check_drive_server', False)
    else:
        print('drive server is ready')
        socketio.emit('check_drive_server', True)


@socketio.on('zumi_stop')
def zumi_stop():
    app.drive_mode.zumi_stop()


@socketio.on('camera_stop')
def drive_mode_camera_stop():
    print('camera should be stopped')
    subprocess.Popen(['fuser', '-k', '3456/tcp'])


@app.route('/gesture')
def gesture():
    return app.send_static_file('index.html')


@socketio.on('open_gesture_drive')
def open_gesture_drive():
    p = subprocess.Popen(
        ['sudo', 'sh', os.path.dirname(os.path.abspath(__file__)) + '/shell_scripts/gesture_drive.sh', '.'])


@socketio.on('gesture_move')
def gesture_move(id):
    if id == 0:
        input_key = "ArrowUp"
    elif id == 1:
        app.drive_mode.zumi_stop()
        return
    elif id == 2:
        input_key = "ArrowLeft"
    elif id == 3:
        input_key = "ArrowRight"
    app.drive_mode.zumi_direction(input_key)


# main ----------------------------------------------------------------------------------------------------
def run(_debug=False):
    socketio.run(app, debug=_debug, host='0.0.0.0',
                 certfile="/usr/local/lib/python3.5/dist-packages/zumidashboard/crt/zumidashboard_ai.crt",
                 keyfile="/usr/local/lib/python3.5/dist-packages/zumidashboard/crt/private.key", port=8443)


if __name__ == '__main__':
    run()
