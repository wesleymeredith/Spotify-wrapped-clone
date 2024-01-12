from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")


# we need to use get_token() in any future headers everytime we want to request 
# from spotify API

def get_token():

# so we need to concat id + secret and transform into base64 for authorization 
    auth_string = client_id + ":" + client_secret

# endcoding
    auth_bytes = auth_string.encode("utf-8")

# base 64 transform, returns b64 object, convert to string, so we can pass to headers for service API
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

# post request to URL    
    headers = {
        "Authorization": "Basic " + auth_base64, #sending in auth data, they will send back the token
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) #return json data in .content field from result object

    #convert to python dict
    json_result = json.loads(result.content)
    token = json_result["access_token"] #parse token stored in a field called "access_token"
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    #set up query
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"] #parse json result
    if len(json_result) == 0:
        print("No artist found...")
        return None
    
    return json_result[0]

def get_current_user(token):

    url = "https://api.spotify.com/v1/me" 
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)    
    print(json_result)


#calls
token = get_token()
result = search_for_artist(token, "Novo Amor") #returns json object/python dict
user = get_current_user(token)

print(user)
