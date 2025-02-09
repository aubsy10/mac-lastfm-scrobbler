import tkinter as tk
from album_scrobble import get_tracklist
from file_handler import check_saved_album
from track_menu import show_track_menu

#Uses the Last.fm api to fetch the tracklist for an album
def fetch_tracklist(root, album_name, artist_name, timestamp, increment, API_KEY, api_token, session_key):
    
    result = get_tracklist(album_name, artist_name, API_KEY, api_token, session_key)
    if result[0] == 0:  
        session_key = result[1]
        tracks = result[2]
        show_track_menu(tracks, root, artist_name, album_name, timestamp, increment, API_KEY, api_token, session_key)
    else:
        session_key = result[1]
        tk.messagebox.showerror("Error", "Album not found or invalid.")

#Initial function used to handle the user choosing the scrobble an album 
def album_submit(root, album_name, artist_name, timestamp, increment, api_key, api_token, session_key):
    
    existing_tracks = check_saved_album(artist_name, album_name)
    
    if existing_tracks:
        show_use_existing_data_menu(root, existing_tracks, artist_name, album_name, timestamp, increment, api_key, api_token, session_key)
    else:
        fetch_tracklist(root, album_name, artist_name, timestamp, increment, api_key, api_token, session_key)

#If existing data exists, this brings up the menu that asks the user if they want to use it
def show_use_existing_data_menu(root, tracklist, artist, album, timestamp, increment, api_key, api_token, session_key):
    overlay = tk.Frame(root, bg="#121212")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    popup = tk.Frame(
        overlay, bg="#1E1E1E", padx=30, pady=30, relief="flat",
        borderwidth=5, highlightbackground="#D1170D", highlightthickness=2
    )
    popup.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        popup, text="Use Existing Scrobble Data?", font=("Helvetica", 14, "bold"),
        fg="#FFFFFF", bg="#1E1E1E"
    ).pack(pady=10)

    def use_existing_data():
        show_track_menu(tracklist, root, artist, album, timestamp, increment, api_key, api_token, session_key)
        close_menu()
        
    def skip_existing_data():
        fetch_tracklist(root, album, artist, timestamp, increment, api_key, api_token, session_key)
        close_menu()
        
    def close_menu():
        overlay.destroy()

    use_button = tk.Button(
        popup, text="Use Data", command=use_existing_data, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#FF3B3B"
    )
    use_button.pack(pady=(20, 5), fill="x")
    
    skip_button = tk.Button(
        popup, text="Skip Existing Data", command=skip_existing_data, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#FF3B3B"
    )
    skip_button.pack(pady=(20, 5), fill="x")

    no_button = tk.Button(
        popup, text="Cancel Scrobble", command=close_menu, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#D1170D"
    )
    no_button.pack(fill="x")