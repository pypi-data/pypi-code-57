import sys
from flask import Flask, send_file, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/selector.html")
def selector():
    return render_template("selector.html", host=sys.argv[1])


@app.route("/app.html")
def apphtml():
    return render_template("app.html")


@app.route("/app.js")
def appjs():
    return send_file("templates/app.js")


@app.route("/viewall.html")
def viewall():
    return render_template("viewall.html", host=sys.argv[1])


@app.route("/stress.html")
def stress():
    return render_template("stress.html", host=sys.argv[1])


app.run("0.0.0.0", port=8080)
