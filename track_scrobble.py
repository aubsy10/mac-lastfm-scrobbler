def scrobble_track(track_name, track_album_name):
    if track_name and track_album_name:
        print(f"Scrobbling Track: {track_name} from {track_album_name}")
    else:
        print("Please fill in all track details.")
