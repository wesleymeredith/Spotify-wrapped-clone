# Wesley Meredith 1-9-2024
# purpose: create a webpage in flask that displays 'Spotify Wrapped' top artists and tracks.

from flask import Flask, request, redirect, url_for, session

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_CODE = os.getenv("TOKEN_CODE")

# create an object so that you can just call it every time
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:5000/redirectPage",
        scope="user-top-read user-library-read"
    )

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirectPage")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')  # returns the token
    token_info = sp_oauth.get_access_token(code)
    return f"<p>{token_info}</p>"
