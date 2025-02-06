import time
import tkinter as tk
import os
from tkinter import ttk
from dotenv import load_dotenv
from auth import get_session_key, sign_in, generate_token
from track_scrobble import scrobble_track
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from utils import decode_filename, get_timestamp
from submit_menu import album_submit
from file_handler import save_track, load_saved_tracks

import tkinter as tk

load_dotenv()
API_KEY = os.getenv("API_KEY")

api_token = generate_token(API_KEY)

after_id = None  # Define this at the start

saved_tracks = []


def create_home_screen():
    # Initialize the main window
    root = tk.Tk()
    root.title("Mac LastFm Scrobbler")
    
    for widget in root.winfo_children():
        widget.destroy()
    
    is_signed_in = False
    global session_key
    
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
        track_filled = track_name_var.get().strip() and track_album_name_var.get().strip() and track_artist_name_var.get().strip()
        
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
        
        if after_id is not None:
            root.after_cancel(after_id)
        
        after_id = root.after(1000, on_album_entry_change)

    def on_album_entry_change(*args):
        typed_text = album_name_var.get().lower()

        if typed_text: 
            matching_albums = [album for album in saved_albums.keys() if typed_text in album.lower()]
            album_dropdown["values"] = matching_albums

            if matching_albums:
                album_dropdown.event_generate("<Down>")
            else:
                album_dropdown.event_generate("<Up>") 
        else:
            album_dropdown["values"] = [] 
            album_dropdown.event_generate("<Up>") 



    def on_album_selected(event):
        selected_album = album_dropdown.get()
        if selected_album in saved_albums:
            artists = saved_albums[selected_album]
            if len(artists) == 1:
                artist_name_var.set(artists[0]) 
            else:
                artist_dropdown["values"] = artists 
        else:
            artist_name_var.set("") 

    def on_artist_selected(event):
        selected_artist = artist_dropdown.get()
        artist_name_var.set(selected_artist)
        
    
    def create_timestamp_section(parent, prefix):
        timestamp_time_frame = tk.Frame(parent, bg="#222")
        timestamp_time_frame.pack(pady=5)

        timestamp_label = tk.Label(timestamp_time_frame, text="Timestamp: ", font=("Arial", 12), fg="white", bg="#222")
        timestamp_label.pack(side="left", padx=5)

        timestamp_entry = DateEntry(timestamp_time_frame, font=("Arial", 12), width=12, background="#444", foreground="white")
        timestamp_entry.pack(side="left", padx=5)

        time_label = tk.Label(timestamp_time_frame, text="Time: ", font=("Arial", 12), fg="white", bg="#222")
        time_label.pack(side="left", padx=5)

        time_frame = tk.Frame(timestamp_time_frame, bg="#222")
        time_frame.pack(side="left")

        def create_time_spinbox(parent, label_text):
            frame = tk.Frame(parent, bg="#222")
            frame.pack(side="left", padx=5)

            label = tk.Label(frame, text=label_text, font=("Arial", 10), fg="white", bg="#222", anchor="center")
            label.pack()

            spinbox = ttk.Spinbox(frame, from_=0, to=59 if label_text != "HH" else 23, width=3, font=("Arial", 12), wrap=True)
            spinbox.pack()
            return spinbox

        hour_spinbox = create_time_spinbox(time_frame, "HH")
        minute_spinbox = create_time_spinbox(time_frame, "MM")
        second_spinbox = create_time_spinbox(time_frame, "SS")
        
        increment_entry = ""
        if(prefix == "album"):
            increment_frame = tk.Frame(timestamp_time_frame, bg="#222")
            increment_frame.pack(side="left", padx=10)

            increment_label = tk.Label(increment_frame, text="Increment (minutes):", font=("Arial", 12), fg="white", bg="#222")
            increment_label.pack(side="top", anchor="w")

            increment_entry = ttk.Entry(increment_frame, width=5, font=("Arial", 12))
            increment_entry.pack()

        return timestamp_entry, hour_spinbox, minute_spinbox, second_spinbox, increment_entry

    ############
    #ALBUM PANEL
    ############
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

    album_timestamp_entry, album_hour_spinbox, album_minute_spinbox, album_second_spinbox, increment_entry = create_timestamp_section(album_panel, "album")
    
    album_submit_button = tk.Button(
        album_panel, text="Scrobble Album", font=("Arial", 12), 
        state=tk.DISABLED,
        command=lambda: album_submit(root, album_name_var.get(), artist_name_var.get(), get_timestamp(album_timestamp_entry.get_date(), f"{album_hour_spinbox.get()}:{album_minute_spinbox.get()}:{album_second_spinbox.get()}")
                                     , increment_entry.get(), API_KEY, api_token, session_key)
    )
    album_submit_button.pack(pady=10)
    
    album_name_var.trace_add("write", lambda *args: update_button_states())
    artist_name_var.trace_add("write", lambda *args: update_button_states())

    # ==============================
    # Panel for Track Scrobble
    # ==============================
    
    global saved_tracks
    saved_tracks = load_saved_tracks()
    
    def delayed_track_update(*args):
        global after_id
        
        if after_id is not None:
            root.after_cancel(after_id)
        
        after_id = root.after(1000, on_track_entry_change)
    
    def on_track_entry_change(*args):
        typed_text = track_name_var.get().lower()

        if typed_text: 
            matching_tracks = [
                track[0] for track in saved_tracks if typed_text in track[0].lower()
            ]
            track_dropdown["values"] = matching_tracks
            
            if matching_tracks:
                track_dropdown.event_generate("<Down>")
            else:
                track_dropdown.event_generate("<Up>")
        else:
            track_dropdown["values"] = [] 
            track_dropdown.event_generate("<Up>")  


    def on_track_selected(event):
        selected_track = track_dropdown.get() 
        if selected_track:
            matching_tracks = [track for track in saved_tracks if track[0] == selected_track]
            if matching_tracks:
                selected_track, album_name, artist_name = matching_tracks[0]

                track_artist_name_var.set(artist_name)
                track_album_name_var.set(album_name)
            else:
                track_artist_name_var.set("") 
                track_album_name_var.set("") 
        else:
            track_artist_name_var.set("") 
            track_album_name_var.set("") 


    track_name_var = tk.StringVar()
    track_album_name_var = tk.StringVar()
    track_artist_name_var = tk.StringVar()

    track_panel = tk.LabelFrame(root, text="Scrobble Track", font=("Arial", 12, "bold"), padx=10, pady=10)
    track_panel.pack(padx=10, pady=10, fill="both", expand=True)

    track_name_label = tk.Label(track_panel, text="Track Name:", font=("Arial", 12))
    track_name_label.pack(pady=5)
    track_dropdown = ttk.Combobox(track_panel, font=("Arial", 12), width=30, textvariable=track_name_var)
    track_dropdown.pack(pady=5)
    track_dropdown.bind("<<ComboboxSelected>>", on_track_selected)
    track_name_var.trace_add("write", delayed_track_update)  # Trigger filtering on text change

    track_album_name_label = tk.Label(track_panel, text="Album Name:", font=("Arial", 12))
    track_album_name_label.pack(pady=5)
    track_album_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30, textvariable=track_album_name_var)
    track_album_name_entry.pack(pady=5)

    track_artist_name_label = tk.Label(track_panel, text="Artist:", font=("Arial", 12))
    track_artist_name_label.pack(pady=5)
    track_artist_name_entry = tk.Entry(track_panel, font=("Arial", 12), width=30, textvariable=track_artist_name_var)
    track_artist_name_entry.pack(pady=5)

    track_save_var = tk.BooleanVar()
    track_save_check = tk.Checkbutton(track_panel, text="Save Track", variable=track_save_var)
    track_save_check.pack(pady=5)
    
    track_timestamp_entry, track_hour_spinbox, track_minute_spinbox, track_second_spinbox, nothing = create_timestamp_section(track_panel, "track")

    
    def handle_track_scrobble(track_name, track_album_name, track_artist_name, timestamp, track_save, api_key, api_token):
        global saved_tracks
        global session_key
        global is_signed_in
        print(f"skey {session_key} is_signed_in {is_signed_in}")
        if(track_save):
            saved_tracks = save_track(track_name, track_album_name, track_artist_name, saved_tracks)
        scrobble_track(track_name, track_album_name, track_artist_name, timestamp, api_key, api_token, session_key)

    track_submit_button = tk.Button(
        track_panel, text="Scrobble Track", font=("Arial", 12), 
        state=tk.DISABLED,
        command=lambda: handle_track_scrobble(track_name_var.get(), track_album_name_var.get(), track_artist_name_var.get(), 
                                       get_timestamp(track_timestamp_entry.get_date(), f"{track_hour_spinbox.get()}:{track_minute_spinbox.get()}:{track_second_spinbox.get()}"), 
                                       track_save_var.get(), API_KEY, api_token)
    )
    track_submit_button.pack(pady=10)
    
    track_name_var.trace_add("write", lambda *args: update_button_states())
    track_album_name_var.trace_add("write", lambda *args: update_button_states())
    track_artist_name_var.trace_add("write", lambda *args: update_button_states())
    
    
    
    # ==============================
    # LASTFM Sign In Button
    # ==============================
    
    def sign_in_handler(API_KEY, api_token):
        global is_signed_in, session_key 
        is_signed_in = sign_in(API_KEY, api_token)
        sign_in_button.config(bg="green", fg="white", text="Signed In")
        time.sleep(5)
        session_key = get_session_key(API_KEY, api_token)
        print(f"sign skey {session_key}")
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





