from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import random

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

def getToken():
    authString = clientID + ":" + clientSecret
    b64_object = authString.encode("utf-8")
    b64_string = str(base64.b64encode(b64_object).decode("utf-8"))

    request_URL = 'https://accounts.spotify.com/api/token'

    headers = {"Authorization": "Basic " + b64_string,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    data = {"grant_type": "client_credentials"}

    response = json.loads(post(request_URL, headers=headers, data=data).content)
    token = response["access_token"]
    return token


def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}


def searchForArtist(token, artistName):
    endpoint = "https://api.spotify.com/v1/search"
    headers = getAuthHeader(token)
    query = f"?q={artistName}&type=artist&limit=1"
    URL = endpoint + query

    obj = json.loads(get(URL, headers=headers).content)
    response = obj["artists"]["items"]
    

    if(len(response) == 0):
        return None
    
    return response[0]


def getSimilarArtists(token, artistID):
    endpoint = f"https://api.spotify.com/v1/artists/{artistID}/related-artists"
    headers = getAuthHeader(token)

    response = json.loads(get(endpoint, headers=headers).content)["artists"]
    return response


def getSimilarArtistsTopTracks(token, artistID):
    endpoint = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?country=US"
    headers = getAuthHeader(token)
    response = json.loads(get(endpoint, headers=headers).content)["tracks"]
    return response

def getCurrentUserTopArtists(token):
    endpoint = 'https://api.spotify.com/v1/me/top/artists'
    headers = getAuthHeader(token)
    response = json.loads(get(endpoint, headers=headers).content)
    return response


token = getToken()
top_artists = getCurrentUserTopArtists(token)
print(top_artists)
artist = searchForArtist(token, input("If you like " ))
id = artist["id"]

similar_artists = getSimilarArtists(token, id)

listOfArtists = [] #Artist id, not name
simArtistTopTrackList = []

print("\nThen you should listen to: ")

for i, similar_artist in enumerate(similar_artists):
    listOfArtists.append(similar_artist['id'])
    print(f"{i+1}. {similar_artist['name']}")


for i in range(len(listOfArtists)):
    temp = getSimilarArtistsTopTracks(token, listOfArtists[i])
    rand = temp[random.randint(0,9)]
    print(f"{i+1}. {rand['name']}")