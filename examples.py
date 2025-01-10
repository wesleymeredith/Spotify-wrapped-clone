import spotipy
import os
import time
import random
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')

app = Flask(__name__)   #Creates an instance of the Flask Class

app.config['SESSION_COOKIE_NAME'] = 'session_name'
app.secret_key = 'your_secret_keys'
TOKEN_INFO = ''

#ROUTES

@app.route('/')
def login():
    authURL = createSpotifyOAuth().get_authorize_url()
    return redirect(authURL)


@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    session['TOKEN_INFO'] = createSpotifyOAuth().get_access_token(code)
    return redirect(url_for('getSimilarArtistsTracks', _external = True))


@app.route('/similarArtistsTracks')
def getSimilarArtistsTracks():
    try:
        token_info = getToken()
    except:
        print('User is not logged in')
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    #Get Artists' ID
    artistName = input("Show me artists that are similar to: ")
    artist = sp.search(q=artistName, type="artist", limit=1)["artists"]["items"]
    id = artist[0]["id"]

    #Get similar artists
    similar_artists = sp.artist_related_artists(id)["artists"]
    listOfArtists = [] #Artist ids, not names

    print(f"Sure, here are some artists that are similar to {artistName}: ")

    for i, similar_artist in enumerate(similar_artists):
        time.sleep(0.4)
        listOfArtists.append(similar_artist['id'])
        print(f"{i+1}. {similar_artist['name']}")

    time.sleep(1)
    answer = input("Would you like me to create a playlist with some of these artists top tracks? ")

    if answer == 'yes' or answer == 'Yes':
        #Get Similar Artists Tracks (URI)
        similar_artists_tracks = []  
        for i in range(len(listOfArtists)):
        #length_of_top_track_list_per_artist = len(sp.artist_top_tracks(artist_id=listOfArtists[i])["tracks"])
            rand = random.randint(0,9)
            similar_artists_tracks.append(sp.artist_top_tracks(artist_id=listOfArtists[i])["tracks"][rand]["id"])
        
        
        #Create Playlist
        user_id = sp.current_user()["id"]
        sp.user_playlist_create(user=user_id, name=f"Top Tracks from Artists Similar to {artistName}", public=True)
        
        playlists = sp.current_user_playlists()['items']
        for playlist in playlists:
            if playlist["name"] == f"Top Tracks from Artists Similar to {artistName}":
                playlist_id = playlist["id"]
            
        sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=similar_artists_tracks)

        return "Success!"
    
    elif answer == 'no' or answer == 'No':
        return "did not want to add playlist"
    
    else:
        return ""
    

def getToken():
    token_info = session.get('TOKEN_INFO', None)
    if not token_info:
        redirect(url_for('login', _external=False))

    current_time = int(time.time())
    is_expired = token_info['expires_at'] - current_time < 60
    if(is_expired):
         token_info = createSpotifyOAuth().refresh_access_token(token_info['refresh_token'])

    return token_info


def createSpotifyOAuth():
    return SpotifyOAuth(
        client_id=clientID, 
        client_secret=clientSecret,
        redirect_uri= url_for('redirect_page',
        _external = True),
        scope='user-library-read playlist-modify-private playlist-modify-public')


app.run(debug=True)