import time
import os
import requests
from auth import get_sig, get_session_key

#Calls the Last.fm api to scrobble the track
def scrobble_track(track_name, track_album_name, track_artist_name, timestamp, api_key, api_token, session_key):
    
    if track_name and track_album_name and track_artist_name:
        
        if session_key is None:
            session_key = get_session_key(api_key,api_token)
        
        params = {
            "api_key": api_key,
            "method": "track.scrobble",
            "artist": track_artist_name, 
            "track": track_name,
            "timestamp": int(timestamp),
            "album": track_album_name,
            "sk": session_key
        }
        
        api_sig = get_sig(params)
        params["api_sig"] = api_sig
        
        response = requests.post("https://ws.audioscrobbler.com/2.0/", params=params)
                       
    else:
        print("Please fill in all track details.")
