# Wesley Meredith 1-9-2024
# purpose: create a webpage in flask that displays 'Spotify Wrapped' top artists and tracks.

from flask import Flask, request, url_for, session, redirect, render_template

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

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