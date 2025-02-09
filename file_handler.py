import os
from utils import encode_filename


TRACK_FILE = "./saved_data/saved_tracks.txt"

#Functions used to handle accessing the files

#Loads the tracks in save_data.txt and adds them to the track list using tuples
def load_saved_tracks():
    tracks = set()
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) == 3:
                    track_name, album_name, artist_name = parts
                    tracks.add((track_name, album_name, artist_name))  
    return tracks
    
#Saves the track in the save_data file
def save_track(track_name, track_album_name, track_artist_name, saved_tracks):
    if saved_tracks is None:
        saved_tracks = set() 
    track_tuple = (track_name, track_album_name, track_artist_name)
    if track_tuple not in saved_tracks:
        with open(TRACK_FILE, "a", encoding="utf-8") as file:
            file.write(f"{track_name} - {track_album_name} - {track_artist_name}\n")
        saved_tracks.add(track_tuple)
        return saved_tracks

#Saves all of the selected tracks in a file for the album
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
            
    with open(TRACK_FILE, "a", encoding="utf-8") as file:
        for track in selected_tracks:
            file.write(f"{track} - {album} - {artist}\n")
            
#Checks the directory to see if an album exists            
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