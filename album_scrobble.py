import requests
import xml.etree.ElementTree as ET
from auth import get_sig, get_session_key

def scrobble_album(album_name, artist_name, scrobble_option, api_key, api_token, session_key):
    if album_name and artist_name:
        print(f"Scrobbling Album: {album_name} by {artist_name} ({scrobble_option})")
        
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
            "method": "album.search",
            "album": album_name
        }
        
        searchResponse = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
        print(searchResponse.text)
        response_bytes = searchResponse.content
        
        try:
        # Remove XML declaration if it exists
            if response_bytes.startswith(b'<?xml'):
                response_bytes = response_bytes.split(b'?>', 1)[1]
            
            # Parse the XML data
            root = ET.fromstring(response_bytes)

            # Namespace handling: register namespaces in the XML parsing
            namespaces = {
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',  # Namespace for opensearch
                'lfm': 'http://www.last.fm/xmlns/'  # Namespace for lfm
            }

            # Find all album elements
            albums = root.findall(".//lfm:albummatches/lfm:album", namespaces)


            # Filter albums by the artist name
            matching_albums = list(filter(lambda album: album.find("artist").text == artist_name, albums))
            
            # Output the result
            if matching_albums:
                print("Artist found:", matching_albums[0].find("name").text)
            else:
                print("Artist not found")

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
        
        #api_sig = get_sig(params)
        #params["api_sig"] = api_sig
        
        
    else:
        print("Please fill in all album details.")
    