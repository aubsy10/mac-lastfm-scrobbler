import time
import requests
from auth import get_sig, get_session_key

def scrobble_track(track_name, track_album_name, track_artist_name, timestamp, api_key, api_token, session_key):
    
    if track_name and track_album_name and track_artist_name:
        print(f"Scrobbling Track: {track_name} from {track_album_name}")
        
        if session_key is None:
            params = {
                "api_key": api_key,
                "method": "auth.getSession",
                "token": api_token
            }
            sk_sig = get_sig(params)
            session_key = get_session_key(api_key,api_token, sk_sig)
        print(f"Skey: {session_key}")
        
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
        print(response)
        if response.status_code == 200:
            print("scrobbled")

           
    else:
        print("Please fill in all track details.")
