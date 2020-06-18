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
import logging, json
from logging.handlers import RotatingFileHandler


if not os.path.isdir('/home/pi/Dashboard/debug'):
    os.mkdir('/home/pi/Dashboard/debug')

app = Flask(__name__, static_url_path="", static_folder='dashboard')
app.zumi = Zumi()
app.screen = Screen(clear=False)
app.user = ''
app.action = ''
app.action_payload = ''
app.wifi_list = set()
app.new_blockly_project = ''
socketio = SocketIO(app)
usr_dir = '/home/pi/Dashboard/user/'
handler = RotatingFileHandler('/home/pi/Dashboard/debug/dashboard.log', maxBytes=10000, backupCount=1)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
lib_dir = os.path.dirname(os.path.abspath(__file__))
app.drive_mode = DriveMode(app.zumi)
app.copy_content = ''
app.knn = ''
app.camera = ''


# dashboard
vendor_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/vendor")
blockly_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/blockly-lib")
ui_library =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/ble-lib")
blockly_fonts =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/fonts")
blockly_images =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/images")
blockly_media =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/media")
blockly_msg =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/msg")

#ide static directories
ide_libjs =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/zumi-ide-poc/dashboard/lib")
ide_mode_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/zumi-ide-poc/dashboard/mode")
ide_lesson_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/zumi-ide-poc/dashboard/lesson")

def _awake():
    app.screen.hello()
    sound.wake_up_sound(app.zumi)


def log(msge):
    app.logger.info(time.strftime('{%Y-%m-%d %H:%M:%S} ')+msge)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ide routes
@app.route('/zumi-ide')
def zumi_ide():
    return app.send_static_file('./zumi-ide-poc/dashboard/index.html')

@app.route('/zumi-ide.js')
def zumi_ide_js():
    return app.send_static_file('./zumi-ide-poc/dashboard/zumi-ide.js')

@app.route('/mode/<path:filename>')
def send_mode_dir(filename):
    return send_from_directory(ide_mode_dir, filename)

@app.route('/lib/<path:filename>')
def send_ide_lib(filename):
    return send_from_directory(ide_libjs, filename)

@app.route('/lesson/<path:filename>')
def send_lesson_dir(filename):
    return send_from_directory(ide_lesson_dir, filename)

# blockly ----------------------------------------------------------------------------------------------------
@app.route('/blockly')
def blockly():
    return app.send_static_file('./blockly/src/app/index.html')


@app.route('/vendor/<path:filename>')
def send_js(filename):
    return send_from_directory(vendor_static_dir, filename)


@app.route('/blockly-lib/<path:filename>')
def send_blocklydir(filename):
    return send_from_directory(blockly_static_dir, filename)


@app.route('/ble-lib/<path:filename>')
def send_ui_dir(filename):
    return send_from_directory(ui_library, filename)


@app.route('/fonts/<path:filename>')
def send_font_dir(filename):
    return send_from_directory(blockly_fonts, filename)


@app.route('/images/<path:filename>')
def send_images_dir(filename):
    return send_from_directory(blockly_images, filename)

@app.route('/media/<path:filename>')
def send_media_dir(filename):
    return send_from_directory(blockly_media, filename)

@app.route('/msg/<path:filename>')
def send_msg_dir(filename):
    return send_from_directory(blockly_msg, filename)


@socketio.on('zumi_run')
def print_message(source_code_base64):
    print('zumi run')
    message_deco = base64.b64decode(source_code_base64)
    print(message_deco)
    new_path = './blockly.py'
    new_days = open(new_path,'w+')

    new_days.write(str(message_deco, 'utf-8'))
    new_days.close()

    p1 = Thread(target = exec_thread, args = ('message_deco2',))
    p1.start()

    # await a successful emit of our reversed message
    # back to the client
    socketio.emit('robolink_run', '')


@socketio.on('check_output')
def check_output():
    print('output function')
    outputPath = './output.txt'
    try:
        outputFile = open(outputPath, 'r')
        content = outputFile.read()
        print(content)
        socketio.emit('hello', content)
    except:
        print('output file not found')


def exec_thread(message_deco):
    print(message_deco)
    try:
        exec("""\n@socketio.on('zumi_run_thread')\nasync def print_message(sid, source_code_base64):\n    global zumiprocess\nlog = open("output.txt", "w")\np = subprocess.Popen(["sudo", "python3", "blockly.py"],stdin=subprocess.PIPE, stdout=log, stderr=log, close_fds=True)\n\n""")
    except Exception as err:
        print("error: ", err)


@socketio.on('stop')
def stop():
    stdoutdata = subprocess.getoutput("sudo kill $(pgrep -f blockly.py)")
    from zumi.zumi import Zumi
    zumi = Zumi()
    print("in emergency function")
    socketio.emit('disconnected', {'msg': 'Connection failed!', 'status': 'false'})


# network connect -------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/select-network')
def select_network():
    return app.send_static_file('index.html')


@app.route('/connect-network')
def connect_network():
    return app.send_static_file('index.html')


@socketio.on('ssid_list')
def ssid_list(sid):
    print('getting ssid list')
    app.action = 'ssid_list'
    log('getting ssid list')

    # _list = scripts.get_ssid_list()
    # app.wifi_list.update(_list.split("\n"))
    # _list = ""
    # for item in app.wifi_list:
    #     _list += item + "\n"
    #
    # socketio.emit('ssid_list', _list)
    # wifi_dict, wifi_list, pw_list = scripts.get_ssid_list()
    wifi_dict = scripts.get_ssid_list()
    # dictionary type
    socketio.emit('ssid_list', wifi_dict)
    # list type
    # socketio.emit('ssid_list', {"wifi_list":wifi_list, "pw_list":pw_list})


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


# confirm check internet msge was receive
@socketio.on('acknowledge_check_internet')
def acknowledge_check_internet():
     log('msge check internet was receive')
     app.action = ''


# connect wifi functions
@socketio.on('connect_wifi')
def connect_wifi(ssid, passwd, isHiddenNetwork):
    print('app.py : connecting wifi start')
    log('app.py : connecting wifi start')
    app.wifi_list.clear()
    print(str(type(ssid))+ssid)
    scripts.add_wifi(ssid, passwd, isHiddenNetwork)
    print("personality start")
    app.screen.draw_image_by_name("tryingtoconnect")
    sound.try_calibrate_sound(app.zumi)
    sound.try_calibrate_sound(app.zumi)
    print("personality done")
    log('app.py : connecting wifi:'+ssid+' end')
    print('app.py : connecting wifi end')


@socketio.on('check_internet')
def check_internet(emiter, language):
    if emiter == 'check_last_network':
        app.action = emiter
    else:
        app.action = 'check_internet'
    connected, ssid = scripts.check_wifi()
    set_backend_language(language)
    if not connected:
        print('emit fail to connect')
        log('app.py : emit fail to connect - Silent Mode')
        if emiter == 'check_internet':
            #app.screen.draw_text_center("Failed to connect.\n Try again.")
            print("FAIL!!!!!")
        socketio.emit(app.action, '')
        return
    time.sleep(5)

    app.connected_to_internet = scripts.check_internet(app.language, ssid)

    if connected:
        if app.connected_to_internet["online_status"] == "captive":
            print('app.py: emit check internet captive portal')
            log('app.py : emit check internet captive portal')
        elif app.connected_to_internet["can_update_dashboard"] or app.connected_to_internet["can_update_content"]:
            app.screen.draw_text_center("I can update")
            print('app.py: emit check internet success')
            log('app.py : emit check internet success')
        socketio.emit(app.action, app.connected_to_internet)

    print(app.connected_to_internet)
    app.action_payload = app.connected_to_internet


def set_backend_language(language):
    korean_key = ["kr", "ko"]
    for item in korean_key:
        if item in language:
            app.language = "ko"
            return
    else:
        app.language = "en"


@socketio.on('zumi_success')
def zumi_success():
    app.screen.draw_text_center("I'm connected to \"" + app.connected_to_internet["network_name"] + "\"")
    sound.calibrated_sound(app.zumi)
    time.sleep(2)
    # _awake()


@socketio.on('kill_supplicant')
def kill_supplicant():
    scripts.kill_supplicant()


@socketio.on('zumi_fail')
def zumi_fail():
    app.screen.draw_text_center("Failed to connect.\n Try again.")
    app.zumi.play_note(Note.A5, 100)
    app.zumi.play_note(Note.F5, 2 * 100)
    time.sleep(2)
    app.screen.draw_text_center("Go to \"zumidashboard.ai\" in your browser")


@socketio.on('open_eyes')
def open_eyes():
    app.screen.hello()


# zumi run demo and lesson event link is in frontend already
@socketio.on('activate_offline_mode')
def activate_offline_mode():
    # usr_dir_path = "/home/pi/Dashboard/off"
    app.screen.draw_text_center("Starting offline mode")
    subprocess.Popen(['sudo', 'killall', 'wpa_supplicant'])
    time.sleep(2)
    # if app.user != "":
    #     app.user = ""
    #     subprocess.call(['sudo', 'pkill', '-9', 'jupyter'])
    #     time.sleep(1)
    #     subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', usr_dir_path])


# are we use this?? ----------------------------------------------------------------------------
@socketio.on('run_demos')
def run_demos():
    print('Run demos event from dashboard')


@socketio.on('goto_lessons')
def goto_lessons():
    print('Go to lessons event from dashboard')


# updater ----------------------------------------------------------------------------------------------------
@app.route('/update')
def update():
    return app.send_static_file('index.html')


@socketio.on('update_firmware')
def update_firmware():
    print('update firmware from dashboard')
    print('server down soon')
    time.sleep(1)
    version = re.findall('[0-9]+.[0-9]+', app.connected_to_internet["latest_dashboard_version"])[0]
    command = "sudo killall -9 python3 && sudo python3 -c 'import zumidashboard.updater as update; "
    command += "update.run(v=\"{}\")'".format(version)
    subprocess.run([command], shell=True)


@socketio.on('update_everything')
def update_everything():
    print('update firmware & content from dashboard')
    print('server down soon')
    time.sleep(1)
    version = re.findall('[0-9]+.[0-9]+', app.connected_to_internet["latest_dashboard_version"])[0]
    command = "sudo killall -9 python3 && sudo python3 -c 'import zumidashboard.updater as update; "
    command += "update.run_everything(v=\"{}\", language=\"{}\")'".format(version, app.language)
    subprocess.run([command], shell=True)


@socketio.on('update_content')
def update_content():
    print('update content from dashboard')
    updater.update_content(app.zumi, app.screen, app.language)
    socketio.emit('update_content')


# for check OS/setup update
def firmware_updater_check(base):
    print("checker")
    if not os.path.isdir(base+'update'):
        os.mkdir(base+'update')
    if not os.path.isfile(base+'update/update_log.txt'):
        f = open(base+'update/update_log.txt','w')
        f.close()

    try:
        update_list = os.listdir(lib_dir + '/update_scripts/')
        for line in open(base + 'update/update_log.txt'):
            try:
                update_list.remove(line.rstrip('\n'))
            except:
                pass

    except FileNotFoundError:
        update_list = []

    if len(update_list):
        firmware_updater(update_list)
        return "updated"
    else:
        return "no update"


# for check OS/setup update
def firmware_updater(update_list):
    print(update_list)
    update_list.sort()
    print(update_list)
    f = open('/home/pi/Dashboard/update/update_log.txt', 'a')
    for version in update_list:
        print("update {}".format(version))
        p = subprocess.Popen(
            ['sudo', 'sh', lib_dir + '/update_scripts/'+version, '.'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        p.wait()
        f.write(version+"\n")


@app.route('/develop')
def develop():
    print('update develop firmware from dashboard')
    print('server down soon')
    time.sleep(1)

    command = "sudo killall -9 python3 && sudo python3 -c 'import zumidashboard.updater as update; update.run_develop()'"
    subprocess.run([command], shell=True)
    return app.send_static_file('index.html')


# main dashboard page related ---------------------------------------------------------------------------------
@app.route('/main')
def step2():
    return app.send_static_file('index.html')


@app.route('/shutting-down')
def shutting_down():
    return app.send_static_file('index.html')


@app.route('/learn')
def learn():
    # update_lessonlist_file()
    return app.send_static_file('index.html')


@app.route('/explore')
def explore():
    return app.send_static_file('index.html')


@app.route('/zumiterminal-8585677100')
def zumiterminal():
    subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', "/home/pi/Desktop"])
    time.sleep(1)
    while True:
        time.sleep(3)
        p = subprocess.Popen(
            ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '5555'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        p.wait()
        if len(stdout) > 1:
            print('jupyter server is not ready')
        else:
            print('jupyter server is ready')
            break

    return "Jupyter has started. <br><br>" \
           "Please go to <a href=\"http://zumidashboard.ai:5555/terminals/1\">" \
           "http://zumidashboard.ai:5555/terminals/1</a> to access the terminal<br>" \
           "Or go to <a href=\"http://zumidashboard.ai:5555\">http://zumidashboard.ai:5555</a> to access Jupyter"


@socketio.on('change_language')
def change_language(language):
    set_backend_language(language)
    try:
        dump_lesson_json(app.user)
    except:
        print("no user detected")


@socketio.on('shutdown')
def shutdown():
    app.screen.draw_text_center("Please switch off after 15 seconds.")
    scripts.shutdown()


@socketio.on('battery_percent')
def battery_percent():
   socketio.emit('battery_percent',str(app.zumi.get_battery_percent()))


@socketio.on('hardware_info')
def hardware_info():
    import psutil, uuid
    from gpiozero import CPUTemperature

    cpu_info = str(int(psutil.cpu_percent()))
    ram_info = str(int(psutil.virtual_memory().percent))
    mac_address = str(':'.join(re.findall('..', '%012x' % uuid.getnode())))
    cpu_temp = CPUTemperature(min_temp=50, max_temp=90)
    cpu_temp_info = str(int(cpu_temp.temperature))
    with open('/home/pi/Dashboard/Zumi_Content_{}/README.md'.format(app.language), 'r') as zumiContentVersionFile:
        content_version = zumiContentVersionFile.readline().replace("\n", "")
    board_version = str(app.zumi.get_board_firmware_version())

    hardward_info = {"cpu_info": cpu_info, "ram_info": ram_info, "mac_address": mac_address,
                     "cpu_temp": cpu_temp_info, "content_version": content_version, "board_version": board_version}

    socketio.emit('hardware_info', hardward_info)
    socketio.emit('battery_percent', str(app.zumi.get_battery_percent()))


# lesson page
@socketio.on('update_lessonlist_file')
def update_lessonlist_file(usr_name):
    dump_lesson_json(usr_name)


def dump_lesson_json(usr_name):
    p = subprocess.Popen(['sudo', 'chown', '-R', 'pi:pi', "/home/pi/Dashboard/user/{}".format(usr_name)])
    p.communicate()
    print("update lesson json")
    lesson_files_path = "/home/pi/Dashboard/user/{}/Zumi_Content_{}/Lesson/".format(usr_name, app.language)
    lesson_folder_files = os.listdir(lesson_files_path)
    lesson_folder_files.sort()
    lesson_list = []
    lesson_id = 0
    for lesson_name in lesson_folder_files:
        if lesson_name[-5:] == 'ipynb':
            with open(lesson_files_path + lesson_name, 'r') as lesson_file:
                file_content = json.loads(lesson_file.read())
            try:
                description = ""
                for p in file_content["cells"][1]["source"]:
                    p = re.sub(r'#+', '', p)
                    description += re.sub(r'<.*?>', '', p)
                    if len(description) > 175:
                        description = description[:175] + "..."
                        break
            except:
                print("something is happen to generate json file")
                description = " "
            lesson_info = {"id": lesson_id, "title": lesson_name[:-6], "description": description}
            lesson_list.append(lesson_info)
            lesson_id += 1
    json_data = {"LessonList": lesson_list}
    with open('{}/dashboard/LessonList.json'.format(lib_dir), 'w') as lesson_list_json_file:
        json.dump(json_data, lesson_list_json_file)


# multiple user ----------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return app.send_static_file('index.html')


@socketio.on('get_users')
def get_users():
    # this is not happen but put in here
    if not os.path.isdir(usr_dir):
        os.makedirs(usr_dir)
    usr_list = os.listdir(usr_dir)
    app.screen.draw_text_center("Please sign in")
    socketio.emit('get_users', usr_list)


@socketio.on('add_user')
def add_user(usr_name):
    add_usr_dir = usr_dir + usr_name
    if os.path.isdir(add_usr_dir):
        # socketio.emit(add_user, False)
        print("user is already exist")
    else:
        os.makedirs(add_usr_dir)
        os.mkdir(add_usr_dir + '/My_Projects')
        os.mkdir(add_usr_dir + '/My_Projects/Jupyter')
        os.mkdir(add_usr_dir + '/My_Projects/Blockly')

        with open("{}/.overlay.json".format(add_usr_dir), "w") as json_file:
            overlaydata = dict()
            overlaydata["main"] = True
            overlaydata["learn"] = True
            json.dump(overlaydata, json_file)
        # for multiple user updater
        app.copy_content = subprocess.Popen(['cp', '-r', '/home/pi/Dashboard/Zumi_Content_'+app.language, add_usr_dir])
        # p.communicate()
        print("generate user : {}".format(usr_name))
        # socketio.emit(add_user, True)


@socketio.on('check_add_user')
def check_add_user():
    if app.copy_content != '':
        poll = app.copy_content.poll()
    else:
        socketio.emit("check_add_user", False)
        return

    if poll is None:
        socketio.emit("check_add_user", False)
    else:
        socketio.emit("check_add_user", True)


@socketio.on('check_overlay')
def check_overlay(user_name):
    current_usr_dir = usr_dir + user_name
    with open("{}/.overlay.json".format(current_usr_dir), "r") as json_file:
        overlay_data = json.load(json_file)
        print(overlay_data)
    socketio.emit('check_overlay', overlay_data)


@socketio.on('start_user')
def start_user(usr_name):
    base_dir_path = "/home/pi/Dashboard/"
    usr_dir_path = base_dir_path + 'user/' + usr_name + '/'

    if app.user != usr_name:
        app.user = usr_name
        subprocess.call(['sudo', 'pkill', '-9', 'jupyter'])
        time.sleep(1)
        subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', usr_dir_path])
    app.screen.draw_text_center("Hello, {}!".format(usr_name))
    time.sleep(1)
    _awake()

    if updater.check_user_content(base_dir_path, usr_dir_path, app.language):
        print("update user's content")
        updater.copy_content(base_dir_path, usr_dir_path, app.language)
        time.sleep(3)
        socketio.emit("need_update_user_content", True)
    else:
        socketio.emit("need_update_user_content", False)

    dump_lesson_json(usr_name)
    # maybe printout something on zumi or reaction


@socketio.on('change_user_name')
def change_user_name(user_names):
    previous_user_dir = usr_dir + user_names[0]
    new_user_dir = usr_dir + user_names[1]
    # if changing name is already exist
    if os.path.isdir(new_user_dir):
        # socketio.emit('change_user_name', False)
        print("changing name {} is already".format(user_names[1]))
    # if current name is not exist
    elif not os.path.isdir(previous_user_dir):
        # socketio.emit('change_user_name', False)
        print("current user {} is not exist".format(user_names[0]))
    else:
        subprocess.Popen(['mv', previous_user_dir, new_user_dir])
        # socketio.emit('change_user_name', False)
        print("change user {} to {}".format(user_names[0], user_names[1]))


@socketio.on('delete_user')
def delete_user(user_name):
    delete_usr_dir = usr_dir + user_name;
    if os.path.isdir(delete_usr_dir):
        subprocess.Popen(['rm', '-r', delete_usr_dir])
        print("user {} is deleted".format(user_name))
        # socketio.emit('delete_user', True)
    else:
        print("user {} is not exist or already deleted".format(user_name))
        # socketio.emit('delete_user', False)

# ---might use later----
# def generate_guest_user():
#     guest_usr_dir = usr_dir + 'guest'
#     os.mkdir(guest_usr_dir)
#     os.mkdir(guest_usr_dir + '/My_Projects')
#     os.mkdir(guest_usr_dir + '/My_Projects/Jupyter')
#     os.mkdir(guest_usr_dir + '/My_Projects/Blockly')
#     subprocess.Popen(['cp', '-r', '/home/pi/Dashboard/Zumi_Content', guest_usr_dir])
#     subprocess.Popen(['sudo', 'chown', '-R', 'pi', guest_usr_dir])


@socketio.on('check_jupyter_server')
def check_jupyter_server():
    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '5555'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        print('jupyter server is not ready')
        socketio.emit('check_jupyter_server', False)
    else:
        print('jupyter server is ready')
        socketio.emit('check_jupyter_server', True)


@socketio.on('overlay_change')
def overlay_change(user_name, item):
    current_usr_dir = usr_dir + user_name
    json_file = open('{}/.overlay.json'.format(current_usr_dir), 'r')
    overlay_data = json.load(json_file)
    overlay_data[item] = False
    json_file.close()
    print(overlay_data)
    with open('{}/.overlay.json'.format(current_usr_dir), 'w') as json_file:
        json.dump(overlay_data, json_file)


# drive mode --------------------------------------------------------------------------------------------------------
@app.route('/drive')
def drive():
    return app.send_static_file('index.html')


@socketio.on('open_drive_mode')
def open_drive_mode():
    p = subprocess.Popen(
        ['sudo', 'sh', os.path.dirname(os.path.abspath(__file__)) + '/shell_scripts/drivemode.sh', '.'])


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


@socketio.on('zumi_direction')
def zumi_direction(input_key):
    app.drive_mode.zumi_direction(input_key)


@socketio.on('zumi_stop')
def zumi_stop():
    app.drive_mode.zumi_stop()


@socketio.on('camera_stop')
def drive_mode_camera_stop():
    print('camera should be stopped')
    subprocess.Popen(['fuser', '-k', '3456/tcp'])


# code mode --------------------------------------------------------------------------------------------------------
@app.route('/code-mode')
def code_mode():
    return app.send_static_file('index.html')


@socketio.on('code_mode')
def code_mode(user_name):

    blockly = os.listdir(usr_dir + '/' + user_name + '/My_Projects/Blockly')
    jupyter = [file.split(".ipynb")[0] for file in os.listdir(usr_dir + '/' + user_name + '/My_Projects/Jupyter') if
               file.endswith(".ipynb")]
    # #code for return [tag, project_name]
    # for x in len(project_list):
    #     tag = re.findall('<[a-z]+>', project_list[x])[0]
    #     project_list[x] = [tag, project_list[x].replace(tag,'')]
    socketio.emit('code_mode', {"jupyter": jupyter, "blockly": blockly})


@socketio.on('create_jupyter')
def create_jupyter(user_name, project_name):
    jupyter_folder = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['cp', lib_dir + '/shell_scripts/Untitled.ipynb', jupyter_folder])
    time.sleep(1)
    subprocess.call(['mv', "{}Untitled.ipynb".format(jupyter_folder), "{}{}.ipynb".format(jupyter_folder, project_name)])
    time.sleep(1.5)
    subprocess.Popen(['sudo', 'chown', '-R', 'pi', jupyter_folder])


@socketio.on('get_blockly_project')
def get_blockly_project(user_name, selected_project):
    print('app: get xml project')
    if app.new_blockly_project:
        app.new_blockly_project = False
        socketio.emit('get_blockly_project', '')
    else:
        project_file = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, selected_project), 'r')
        socketio.emit('get_blockly_project', str(project_file.read()))


@socketio.on('save_blockly_file')
def save_blockly_file(user_name, project_name, xml_content):
    print('app: saving blockly file')
    myfile = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, project_name), 'w')
    myfile.write(xml_content)
    myfile.close()


@socketio.on('create_blockly')
def create_blockly(user_name, project_name):
    app.new_blockly_project = True
    # need to copy from blank project xml file
    myfile = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, project_name), 'w')
    myfile.close()


@socketio.on('rename_blockly')
def rename_blockly(user_name, project_name, new_name):
    blockly_dir = "{}/My_Projects/Blockly/".format(usr_dir + user_name)
    subprocess.call(['mv', "{}.xml".format(blockly_dir+project_name), "{}.xml".format(blockly_dir+new_name)])
    time.sleep(1)

@socketio.on('rename_jupyter')
def rename_jupyter(user_name, project_name, new_name):
    jupyter_dir = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['mv', "{}.ipynb".format(jupyter_dir+project_name), "{}.ipynb".format(jupyter_dir+new_name)])
    time.sleep(1)

@socketio.on('delete_blockly')
def delete_blockly(user_name, project_name):
    blockly_dir = "{}/My_Projects/Blockly/".format(usr_dir + user_name)
    subprocess.call(['rm',"-rf", "{}.xml".format(blockly_dir + project_name)])
    time.sleep(1)

@socketio.on('delete_jupyter')
def delete_jupyter(user_name, project_name):
    blockly_dir = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['rm',"-rf", "{}.ipynb".format(blockly_dir + project_name)])
    time.sleep(1)


# wizards -------------------------------------------------------------------------------------------------
@app.route('/regression')
def regression():
    return app.send_static_file('index.html')


@socketio.on('drive_regression')
def drive_regression(seconds):
    app.zumi.forward(duration=seconds)


@app.route('/knn')
def knn():
    return app.send_static_file('index.html')


@socketio.on('start_knn')
def start_knn():
    from zumi.util.color_classifier import ColorClassifier
    app.knn = ColorClassifier()
    app.knn.demo_name = "tmp"
    app.knn.data_file_name = app.knn.demo_name + "_KNN_data"


@socketio.on('knn_label_list')
def knn_label_list(label_list):
    print(len(label_list))
    app.knn.label_num = len(label_list)
    for label in label_list:
        app.knn.label_names.append(label)
        app.knn.label_keys.append(label)


@socketio.on('knn_add_data')
def knn_add_data(label_name):
    frame = app.drive_mode.camera.capture()
    print(frame)


@app.route('/knn/camera-screen/')
def knn_camera_screen():
    return app.send_static_file('./knn-camera/index.html')


def gen():
    import cv2
    while True:
        frame = app.camera.capture()
        app.frame = frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        (flag, encodedImage) = cv2.imencode('.jpg', frame)
        if not flag:
            continue
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route('/video_feed')
def video_feed():
    print('load video feed')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')



# main ----------------------------------------------------------------------------------------------------
def run(_debug=False):
    if not os.path.isfile('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json'):
        subprocess.run(["sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json"], shell=True)
    firmware_updater_check('/home/pi/Dashboard/')

    subprocess.run('sudo python3 /usr/local/lib/python3.5/dist-packages/zumidashboard/gesture.py & 2>&1', shell=True)

    socketio.run(app, debug=_debug, host='0.0.0.0', port=80)


if __name__ == '__main__':
    run()
