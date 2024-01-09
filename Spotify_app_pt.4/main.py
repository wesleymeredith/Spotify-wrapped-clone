# Wesley Meredith 1-9-2024
# purpose: create a webpage in flask that displays 'Spotify Wrapped' top artists and tracks.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    return "<p>Hello, World!</p>"

@app.route("/redirectPage")
def redirectPage():
    return "<p>Hello, World!</p>"

@app.route("/display")
def display():
    return "<p>Hello, World!</p>"