import os
from utils import encode_filename

def save_selected_tracks(selected_tracks, artist, album):
    directory = "./saved_data/saved_albums"
    os.makedirs(directory, exist_ok=True)
    
    encoded_album = encode_filename(album)
    encoded_artist = encode_filename(artist)
    
    filename = f"{encoded_album}-{encoded_artist}.txt".replace(" ", "_")
    filepath = os.path.join(directory, filename)
    
    with open(filepath, "w", encoding="utf-8") as file:
        for track in selected_tracks:
            file.write(track + "\n")
            
            
def check_saved_album(artist, album):
    directory = "./saved_data/saved_albums"
    encoded_album = encode_filename(album)
    encoded_artist = encode_filename(artist)
    
    filename = f"{encoded_album}-{encoded_artist}.txt".replace(" ", "_")
    filepath = os.path.join(directory, filename)
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            tracks = [line.strip() for line in file.readlines()]
        return tracks
    return None