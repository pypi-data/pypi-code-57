from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import time, subprocess
from subprocess import PIPE

from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.util.camera import Camera
import zumidashboard.scripts as scripts
import zumidashboard.sounds as sound
import os

from threading import Thread

app = Flask(__name__, static_url_path="", static_folder='dashboard')
app.zumi = Zumi()
app.screen = Screen(clear=False)
app.camera = Camera()
app.ssid = ''
app.current_key = ''
app.drive_thread = ''
socketio = SocketIO(app)

global esta_verde 
global heading
heading = 0

@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/select-network')
def select_network():
    return app.send_static_file('index.html')


@socketio.on('ssid_list')
def ssid_list(sid):
    print('getting ssid list')
    _list = scripts.get_ssid_list()
    socketio.emit('ssid_list',str(_list))


# connect wifi functions
@socketio.on('connect_wifi')
def connect_wifi(ssid, passwd):
    print('app.py : connecting wifi start')
    print(ssid)
    scripts.add_wifi(ssid, passwd)
    print("personality start")
    app.screen.draw_image_by_name("tryingtoconnect")
    sound.try_calibrate_sound(app.zumi)
    sound.try_calibrate_sound(app.zumi)
    print("personality done")
    print('app.py : connecting wifi end')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@socketio.on('stop')
def stop():
    print("killing process")
    stdoutdata = subprocess.getoutput("sudo kill $(pgrep -f /home/pi/wizard-development/blockly.py)")
    app.zumi = Zumi()

@socketio.on('send_file')
def send_file(file):
    print("received file")
    run_file = open("blockly.py", 'w+')
    run_file.write(file)
    run_file.close()
    print("about to run subprocess")
    output = subprocess.getoutput("sudo python3 /home/pi/wizard-development/blockly.py &")
    #subprocess.call("sudo python3 /home/pi/zumboy/dev/codemirror/blockly.py &", shell=True)
    #result=subprocess.run(["sudo python3 /home/pi/zumboy/dev/codemirror/blockly.py &"], shell=True, stdout=PIPE)
    #result = result.stderr
    socketio.emit("output", output)
    print("finished")


def run(_debug=False):
    if not os.path.isfile('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json'):
        subprocess.run(["sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json"], shell=True)

    #socketio.run(app,debug=_debug, host='0.0.0.0', port=80)
    #socketio.run(app, debug=_debug, host='0.0.0.0', port=80, ssl_context=('host.cert', 'host.key'))
    socketio.run(app,debug=_debug, host='0.0.0.0', certfile="host.cert", keyfile="host.key", port=443)
if __name__ == '__main__':
    run()

