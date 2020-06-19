import sys
import threading
import logging
import webbrowser
import pathlib
import tkinter
import tkinter.filedialog

from flask import Flask, send_file, request, jsonify, render_template
from .. import manager

app = Flask(__name__)

# Suppress excessive Flask logging to make the console usable by KeypadDriver
logging.getLogger("werkzeug").setLevel(logging.WARNING)

manager = manager.Manager()


@app.route("/")
def index():
    return render_template("index.html", manager=manager)


@app.route("/static/index.css")
def staticfile():
    return send_file("templates/index.css")


@app.route("/static/index.js")
def staticjs():
    return send_file("templates/index.js")


@app.route("/driver", methods=["POST"])
def driver():
    data = request.json
    manager.chooseDriver(manager.drivers[data["driver"]])
    return ""


@app.route("/script", methods=["POST"])
def script():
    data = request.json
    manager.chooseScript(manager.scripts[data["script"]])
    return ""


@app.route("/relay", methods=["POST"])
def relay():
    data = request.json
    manager.connect(data["host"], (data["psk"] if "psk" in data else None))
    return ""


@app.route("/status")
def status():
    return jsonify(manager.getStatus())


if len(sys.argv) < 2:
    root = tkinter.Tk()
    root.withdraw()
    configdir = tkinter.filedialog.askdirectory(initialdir=pathlib.Path.home())
    root.destroy()
else:
    configdir = sys.argv[1]

manager.configure(configdir)

appthread = threading.Thread(target=app.run)
appthread.start()

webbrowser.open("http://localhost:5000")

manager.run()
