# Wesley Meredith 1-9-2024
# purpose: create a webpage in flask that displays 'Spotify Wrapped' top artists and tracks.

from flask import Flask, request, redirect, url_for, session, render_template

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
def index():
    name ='username'
    return render_template('index.html', title='Welcome', username=name)

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



@app.route("/display", methods=["GET", "POST"])
def display():
    user_token = get_token()

    if user_token is None:
        return "User not authenticated. Please log in first."

    access_token = user_token.get('access_token')

    if access_token is None:
        return "Access token not found. Please log in again."

    sp = spotipy.Spotify(auth=access_token)
    
    user_top_artists = sp.current_user_top_artists(
        limit=20,
        offset=0,
        time_range="short_term"
    )
    user_top_artists_MEDIUM = sp.current_user_top_artists(
        limit=20,
        offset=0,
        time_range="medium_term"
    )
    user_top_artists_LONG = sp.current_user_top_artists(
        limit=20,
        offset=0,
        time_range="long_term"
    )


    user_top_artists = [artist['name'] for artist in user_top_artists['items']]
    user_top_artists_MEDIUM = [artist['name'] for artist in user_top_artists_MEDIUM['items']]
    user_top_artists_LONG = [artist['name'] for artist in user_top_artists_LONG['items']]
    
    if request.method == "POST":
        time_range = request.form.get("time_range")
        recommendations = get_recommendations(sp, user_top_artists)
        return render_template('display.html', title='Welcome', user_top_artists=user_top_artists, user_top_artists_MEDIUM=user_top_artists_MEDIUM, user_top_artists_LONG=user_top_artists_LONG, recommendations=recommendations)


    return render_template('display.html', title='Welcome', user_top_artists=user_top_artists, user_top_artists_MEDIUM=user_top_artists_MEDIUM,user_top_artists_LONG=user_top_artists_LONG)


# Function to get recommendations based on user's top artists
def get_recommendations(sp, artists):
    recommendations = []
    for artist in artists:
        results = sp.recommendations(seed_artists=[artist['id']], limit=10)
        recommendations.extend(results['tracks'])
    return recommendations

# for track in results['tracks']:
#         logger.info('Recommendation: %s - %s', track['name'],
#                     track['artists'][0]['name'])