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
app.secret_key = os.getenv("SECRET_KEY")

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
    session.clear()
    code = request.args.get('code')  # returns the token
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_CODE] = token_info    
    return redirect(url_for("display", _external=True))

#f"<p>{token_info}</p>"

def get_token(): 
    token_info = session.get(TOKEN_CODE, None)
    return token_info


@app.route("/display")
def display():
    user_token = get_token()

    if user_token is None:
        return "User not authenticated. Please log in first."

    access_token = user_token.get('access_token')

    if access_token is None:
        return "Access token not found. Please log in again."

    sp = spotipy.Spotify(auth=access_token)
    
    user_top_songs = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="medium_term"
    )

    return str(user_top_songs['items'])


# @app.route("/display")
# def display():
#     user_token=get_token()
#     sp = spotipy.Spotify(
#         auth=user_token['access_token']
#     )
#     user_top_songs = sp.current_user_top_tracks(
#         limit=10,
#         offset=0,
#         time_range="medium_term"
#     )
#     return str(user_top_songs['items'])
