import time
import tkinter as tk
import os
from tkinter import ttk
from dotenv import load_dotenv
from auth import sign_in, generate_token
from track_scrobble import scrobble_track
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from utils import decode_filename, get_timestamp
from submit_menu import album_submit

import tkinter as tk

load_dotenv()
API_KEY = os.getenv("API_KEY")

session_key = None
api_token = generate_token(API_KEY)

after_id = None  # Define this at the start


def create_home_screen():
    # Initialize the main window
    root = tk.Tk()
    root.title("Mac LastFm Scrobbler")
    
    for widget in root.winfo_children():
        widget.destroy()
    
    is_signed_in = False
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

    def update_button_states():
        global is_signed_in

        album_filled = album_name_var.get().strip() and artist_name_var.get().strip()
        track_filled = track_name_entry.get().strip() and track_album_name_entry.get().strip() and track_artist_name_entry.get().strip()
        
        album_submit_button.config(state=tk.NORMAL if album_filled and is_signed_in else tk.DISABLED)
        track_submit_button.config(state=tk.NORMAL if track_filled and is_signed_in else tk.DISABLED)
    
    # ==============================
    # Panel for Album Scrobble
    # ==============================
    
    def load_saved_albums():
        directory = "./saved_data/saved_albums"
        albums_dict = {}  # {decoded_album_name: [decoded_artist1, decoded_artist2, ...]}

        if not os.path.exists(directory):
            return albums_dict

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                try:
                    encoded_album, encoded_artist = filename.rsplit("-", 1)
                    album = decode_filename(encoded_album.replace(".txt", "")).replace("_", " ")
                    artist = decode_filename(encoded_artist.replace(".txt", "")).replace("_", " ")

                    if album not in albums_dict:
                        albums_dict[album] = []
                    albums_dict[album].append(artist)
                except ValueError:
                    continue 

        return albums_dict

    saved_albums = load_saved_albums()

    def delayed_update(*args):
        global after_id
        
        # Cancel the previous scheduled update if any
        if after_id is not None:
            root.after_cancel(after_id)
        
        # Schedule the new update after 200ms (adjustable delay)
        after_id = root.after(1000, on_album_entry_change)

    def on_album_entry_change(*args):
        typed_text = album_name_var.get().lower()

        if typed_text:  # Only filter when text is entered
            matching_albums = [album for album in saved_albums.keys() if typed_text in album.lower()]
            album_dropdown["values"] = matching_albums

            # Automatically open the dropdown if there are matches
            if matching_albums:
                album_dropdown.event_generate("<Down>")  # This simulates pressing the Down arrow to open the dropdown
            else:
                album_dropdown.event_generate("<Up>")  # If no matches, you might want to close or hide the dropdown
        else:
            album_dropdown["values"] = []  # Clear suggestions when empty
            album_dropdown.event_generate("<Up>")  # Optionally close the dropdown when the field is empty



    def on_album_selected(event):
        selected_album = album_dropdown.get()  # Use the dropdown's selected value
        if selected_album in saved_albums:
            artists = saved_albums[selected_album]
            if len(artists) == 1:
                artist_name_var.set(artists[0])  # Autofill if only one artist
            else:
                artist_dropdown["values"] = artists  # Allow artist selection
        else:
            artist_name_var.set("")  # Clear if album is removed

    def on_artist_selected(event):
        selected_artist = artist_dropdown.get()
        artist_name_var.set(selected_artist)

    # Initialize the variables and UI components
    album_name_var = tk.StringVar()
    artist_name_var = tk.StringVar()

    album_panel = tk.LabelFrame(root, text="Scrobble Album", font=("Arial", 12, "bold"), padx=10, pady=10)
    album_panel.pack(padx=10, pady=10, fill="both", expand=True)

    album_name_label = tk.Label(album_panel, text="Album Name:", font=("Arial", 12))
    album_name_label.pack(pady=5)

    album_dropdown = ttk.Combobox(album_panel, font=("Arial", 12), width=30, textvariable=album_name_var)
    album_dropdown.pack(pady=5)
    album_dropdown.bind("<<ComboboxSelected>>", on_album_selected)
    album_name_var.trace_add("write", delayed_update)  # Trigger delayed update on text change

    artist_name_label = tk.Label(album_panel, text="Artist Name:", font=("Arial", 12))
    artist_name_label.pack(pady=5)

    artist_dropdown = ttk.Combobox(album_panel, font=("Arial", 12), width=30, textvariable=artist_name_var)
    artist_dropdown.pack(pady=5)
    artist_dropdown.bind("<<ComboboxSelected>>", on_artist_selected)

    
    timestamp_label = tk.Label(album_panel, text="Timestamp (YYYY-MM-DD):", font=("Arial", 12))
    timestamp_label.pack(pady=5)
    timestamp_entry = DateEntry(album_panel, font=("Arial", 12), width=30)
    timestamp_entry.pack(pady=5)

    time_label = tk.Label(album_panel, text="Time (HH:MM:SS):", font=("Arial", 12))
    time_label.pack(pady=5)

    time_frame = tk.Frame(album_panel)
    time_frame.pack(pady=5)

    hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=3, font=("Arial", 12), wrap=True)
    hour_spinbox.pack(side="left", padx=5)

    minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=3, font=("Arial", 12), wrap=True)
    minute_spinbox.pack(side="left", padx=5)

    second_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=3, font=("Arial", 12), wrap=True)
    second_spinbox.pack(side="left", padx=5)

    album_submit_button = tk.Button(
        album_panel, text="Scrobble Album", font=("Arial", 12), 
        state=tk.DISABLED,
        command=lambda: album_submit(root, album_name_var.get(), artist_name_var.get(), get_timestamp(timestamp_entry.get_date(), f"{hour_spinbox.get()}:{minute_spinbox.get()}:{second_spinbox.get()}"), api_token)
    )
    album_submit_button.pack(pady=10)
    
    album_name_var.trace_add("write", lambda *args: update_button_states())
    artist_name_var.trace_add("write", lambda *args: update_button_states())

    # ==============================
    # Panel for Track Scrobble
    # ==============================
    
    track_name_var = tk.StringVar()
    track_album_name_var = tk.StringVar()
    track_artist_name_var = tk.StringVar()
    
    track_panel = tk.LabelFrame(root, text="Scrobble Track", font=("Arial", 12, "bold"), padx=10, pady=10)
    track_panel.pack(padx=10, pady=10, fill="both", expand=True)

    track_name_label = tk.Label(track_panel, text="Track Name:", font=("Arial", 12))
    track_name_label.pack(pady=5)
    track_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30, textvariable=track_name_var)
    track_name_entry.pack(pady=5)

    track_album_name_label = tk.Label(track_panel, text="Album Name:", font=("Arial", 12))
    track_album_name_label.pack(pady=5)
    track_album_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30, textvariable=track_album_name_var)
    track_album_name_entry.pack(pady=5)
    
    track_artist_name_label = tk.Label(track_panel, text="Artist:", font=("Arial", 12))
    track_artist_name_label.pack(pady=5)
    track_artist_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30, textvariable=track_artist_name_var)
    track_artist_name_entry.pack(pady=5)

    track_submit_button = tk.Button(
        track_panel, text="Scrobble Track", font=("Arial", 12), 
        state=tk.DISABLED,
        command=lambda: scrobble_track(track_name_var.get(), track_album_name_var.get(), track_artist_name_var, int(time.time()), api_token)
    )
    track_submit_button.pack(pady=10)
    
    track_name_var.trace_add("write", lambda *args: update_button_states())
    track_album_name_var.trace_add("write", lambda *args: update_button_states())
    track_artist_name_var.trace_add("write", lambda *args: update_button_states())
    
    # ==============================
    # LASTFM Sign In Button
    # ==============================
    
    def sign_in_handler(API_KEY, api_token):
        global is_signed_in 
        is_signed_in = sign_in(API_KEY, api_token)
        sign_in_button.config(bg="green", fg="white", text="Signed In")
        update_button_states()
        
        
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





