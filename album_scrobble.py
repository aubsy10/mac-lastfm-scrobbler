def scrobble_album(album_name, artist_name, scrobble_option):
    if album_name and artist_name:
        print(f"Scrobbling Album: {album_name} by {artist_name} ({scrobble_option})")
    else:
        print("Please fill in all album details.")