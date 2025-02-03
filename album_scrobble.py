import requests
import re
import xml.etree.ElementTree as ET
from auth import get_session_key
from track_scrobble import scrobble_track

def get_tracklist(album_name, artist_name, api_key, api_token, session_key):
    if album_name and artist_name:
        
        if session_key is None:
            session_key = get_session_key(api_key,api_token)
        
        if validate_album(album_name, artist_name, api_key):
            tracks = get_album_info(album_name, artist_name, api_key)
            return(0,session_key, tracks)
        else:
            return (1, session_key)
        
        #api_sig = get_sig(params)
        #params["api_sig"] = api_sig  
    else:
        print("Please fill in all album details.")

def validate_album(album_name, artist_name, api_key):
    params = {
        "api_key": api_key,
        "method": "album.search",
        "album": album_name,
    }
        
    searchResponse = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
    response_text = searchResponse.text  
    
    if response_text.startswith('<?xml'):
        response_text = response_text.split('?>', 1)[1]
        
    response_text_clean = re.sub(r'\sxmlns="[^"]+"', '', response_text)  # Remove default namespace
    response_text_clean = re.sub(r'(<\/?)[a-zA-Z0-9]+:', r'\1', response_text_clean)  # Remove prefixes

    # Now parse the cleaned XML
    root = ET.fromstring(response_text_clean)

    album_matches = root.find('results/albummatches')

    if album_matches is not None:
        for album in album_matches.findall('album'):
            artist = album.find('artist').text
            album_title = album.find('name').text
            #album_url = album.find('url').text

            if album_title.lower() == album_name.lower() and artist.lower() == artist_name.lower():
                return True
    
    return False

def get_album_info(album_name, artist_name, api_key):
    params = {
        "api_key": api_key,
        "method": "album.getInfo",
        "album": album_name,
        "artist": artist_name
    }
    
    searchResponse = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
    
    response_text = searchResponse.text  
    
    print(response_text)
    
    if response_text.startswith('<?xml'):
        response_text = response_text.split('?>', 1)[1]
        
    response_text_clean = re.sub(r'\sxmlns="[^"]+"', '', response_text)  # Remove default namespace
    response_text_clean = re.sub(r'(<\/?)[a-zA-Z0-9]+:', r'\1', response_text_clean)  # Remove prefixes
    
    root = ET.fromstring(response_text_clean)
    
    rettracks = []
    tracks = root.findall('.//track/name')
    for track in tracks:
        rettracks.append(track.text)
    
    return rettracks

def scrobble_album(selected_tracks, artist_name, album_name, timestamp, api_key, api_token, session_key):
    print(f"scrobbling {selected_tracks} on {album_name} by {artist_name} at {timestamp}")
    
    if session_key is None:
        session_key = get_session_key(api_key,api_token)
        
    for track in selected_tracks:
        scrobble_track(track, album_name, artist_name, timestamp, api_key, api_token, session_key)
    
    return session_key
    