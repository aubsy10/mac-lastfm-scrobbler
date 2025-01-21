import tkinter as tk
import os
from dotenv import load_dotenv
from auth import sign_in_handler, generate_token, get_sig
from album_scrobble import scrobble_album
from track_scrobble import scrobble_track

load_dotenv()
API_KEY = os.getenv("API_KEY")

session_key = None

def create_home_screen():
    # Initialize the main window
    root = tk.Tk()
    root.title("Mac LastFm Scrobbler")
    
    api_token = generate_token(API_KEY)
    
    print("Generated Token:", api_token)

    # Set window size to be a portion of the screen
    screen_width = root.winfo_screenwidth()  # Get screen width
    screen_height = root.winfo_screenheight()  # Get screen height
    window_width = int(screen_width * 0.7)  # 60% of screen width
    window_height = int(screen_height * 0.8)  # 60% of screen height

    # Center the window
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
    
    # ==============================
    # Panel for Album Scrobble
    # ==============================
    album_panel = tk.LabelFrame(root, text="Scrobble Album", font=("Arial", 12, "bold"), padx=10, pady=10)
    album_panel.pack(padx=10, pady=10, fill="both", expand=True)

    album_name_label = tk.Label(album_panel, text="Album Name:", font=("Arial", 12))
    album_name_label.pack(pady=5)
    album_name_entry = tk.Entry(album_panel, font=("Arial", 12), width=30)
    album_name_entry.pack(pady=5)

    artist_name_label = tk.Label(album_panel, text="Artist Name:", font=("Arial", 12))
    artist_name_label.pack(pady=5)
    artist_name_entry = tk.Entry(album_panel, font=("Arial", 12), width=30)
    artist_name_entry.pack(pady=5)

    scrobble_option_var = tk.StringVar(value="Top Tracks")
    scrobble_option_top_tracks = tk.Radiobutton(
        album_panel, text="Top Tracks", variable=scrobble_option_var, value="Top Tracks", font=("Arial", 12)
    )
    scrobble_option_top_tracks.pack(pady=5)

    scrobble_option_entire_album = tk.Radiobutton(
        album_panel, text="Entire Album", variable=scrobble_option_var, value="Entire Album", font=("Arial", 12)
    )
    scrobble_option_entire_album.pack(pady=5)

    album_submit_button = tk.Button(
        album_panel, text="Scrobble Album", font=("Arial", 12), 
        command=lambda: scrobble_album(album_name_entry.get(), artist_name_entry.get(), scrobble_option_var.get(), API_KEY, api_token, session_key)
    )
    album_submit_button.pack(pady=10)

    # ==============================
    # Panel for Track Scrobble
    # ==============================
    track_panel = tk.LabelFrame(root, text="Scrobble Track", font=("Arial", 12, "bold"), padx=10, pady=10)
    track_panel.pack(padx=10, pady=10, fill="both", expand=True)

    track_name_label = tk.Label(track_panel, text="Track Name:", font=("Arial", 12))
    track_name_label.pack(pady=5)
    track_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30)
    track_name_entry.pack(pady=5)

    track_album_name_label = tk.Label(track_panel, text="Album Name:", font=("Arial", 12))
    track_album_name_label.pack(pady=5)
    track_album_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30)
    track_album_name_entry.pack(pady=5)
    
    track_artist_name_label = tk.Label(track_panel, text="Artist:", font=("Arial", 12))
    track_artist_name_label.pack(pady=5)
    track_artist_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30)
    track_artist_name_entry.pack(pady=5)

    track_submit_button = tk.Button(
        track_panel, text="Scrobble Track", font=("Arial", 12), 
        command=lambda: scrobble_track(track_name_entry.get(), track_album_name_entry.get(), track_artist_name_entry.get(), API_KEY, api_token, session_key)
    )
    track_submit_button.pack(pady=10)

    # ==============================
    # Last.fm Sign-In Button
    # ==============================
    sign_in_button = tk.Button(
        root, text="Sign In to Last.fm", font=("Arial", 12), width=20, height=2, 
        bg="#E70010", fg="red", relief="flat", 
        command=lambda: sign_in_handler(API_KEY, api_token)
    )
    sign_in_button.pack(pady=15)
    

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    create_home_screen()





