import tkinter as tk
import os
from tkinter import ttk
from dotenv import load_dotenv
from auth import sign_in_handler, generate_token, get_sig
from album_scrobble import get_tracklist
from track_scrobble import scrobble_track
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

session_key = None
api_token = generate_token(API_KEY)

def show_track_menu(tracks, root, artist, album, timestamp):
    overlay = tk.Frame(root, bg="#121212")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    popup = tk.Frame(
        overlay, bg="#1E1E1E", padx=30, pady=30, relief="flat",
        borderwidth=5, highlightbackground="#D1170D", highlightthickness=2
    )
    popup.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        popup, text="Select Tracks to Scrobble", font=("Helvetica", 14, "bold"),
        fg="#FFFFFF", bg="#1E1E1E"
    ).pack(pady=10)

    track_frame = tk.Frame(popup, bg="#1E1E1E", height=200)
    track_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(track_frame, bg="#1E1E1E", highlightthickness=0)
    scrollbar = tk.Scrollbar(track_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_mouse_wheel(event):
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")  
        else:
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    checkboxes = {}  # Define checkboxes after creating track checkboxes

    def track_selection_changed():
            if any(data["var"].get() == False for data in checkboxes.values()):
                select_all_var.set(False)
            else:
                select_all_var.set(True)

    # Creating checkboxes for existing tracks
    for track in tracks:
        var = tk.BooleanVar()

        row_frame = tk.Frame(scrollable_frame, bg="#1E1E1E")
        row_frame.pack(fill="x", padx=10, pady=2, anchor="w")

        track_label = tk.Label(
            row_frame, text=track, font=("Helvetica", 12),
            fg="#FFFFFF", bg="#1E1E1E", anchor="w"
        )
        track_label.pack(side="left", padx=5)

        cb = tk.Checkbutton(
            row_frame, variable=var, bg="#1E1E1E", activebackground="#D1170D",
            selectcolor="#D1170D", fg="#FFFFFF"
        )
        cb.pack(side="right", padx=5)

        remove_button = tk.Button(
            row_frame, text="Remove", font=("Helvetica", 10),
            background="#FFFFFF", foreground="#D1170D", relief="flat",
            activebackground="#FFFFFF",
            command=lambda track=track: remove_track(track)
        )
        remove_button.pack(side="right", padx=5)

        checkboxes[track] = {"var": var, "checkbox": cb, "remove_button": remove_button, "row_frame": row_frame}

        var.trace_add("write", lambda *args: track_selection_changed())

    def add_track():
        new_track = new_track_entry.get().strip()
        if new_track and new_track not in checkboxes:
            var = tk.BooleanVar()
            row_frame = tk.Frame(scrollable_frame, bg="#1E1E1E")
            row_frame.pack(fill="x", padx=10, pady=2, anchor="w")

            track_label = tk.Label(
                row_frame, text=new_track, font=("Helvetica", 12),
                fg="#FFFFFF", bg="#1E1E1E", anchor="w"
            )
            track_label.pack(side="left", padx=5)

            cb = tk.Checkbutton(
                row_frame, variable=var, bg="#1E1E1E", activebackground="#D1170D",
                selectcolor="#D1170D", fg="#FFFFFF"
            )
            cb.pack(side="right", padx=5)

            remove_button = tk.Button(
                row_frame, text="Remove", font=("Helvetica", 10),
                background="#FFFFFF", foreground="#D1170D", relief="flat",
                activebackground="#FFFFFF",
                command=lambda track=new_track: remove_track(track)
            )
            remove_button.pack(side="right", padx=5)

            checkboxes[new_track] = {"var": var, "checkbox": cb, "remove_button": remove_button, "row_frame": row_frame}
            new_track_entry.delete(0, tk.END)

            var.trace_add("write", lambda *args: track_selection_changed())  # Bind the new track checkbox to the selection change function

    def remove_track(track):
        if track in checkboxes:
            checkboxes[track]["row_frame"].destroy()
            del checkboxes[track]
            
    select_all_var = tk.BooleanVar()

    def select_all_tracks():
        value = select_all_var.get() 
        for track, data in checkboxes.items():
            data["var"].set(value)

    select_all_cb = tk.Checkbutton(
        popup, variable=select_all_var, text="Select All", font=("Helvetica", 12), 
        bg="#1E1E1E", activebackground="#D1170D", selectcolor="#D1170D", fg="#FFFFFF",
        command=select_all_tracks
    )
    select_all_cb.pack(pady=5)

    new_track_entry = tk.Entry(popup, font=("Helvetica", 12), bg="#333333", fg="white", insertbackground="white")
    new_track_entry.pack(pady=10, fill="x")
    
    add_button = tk.Button(
    popup, text="Add Track", command=add_track, bg="#FFFFFF", fg="#D1170D",
    font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, borderwidth=0,
    activebackground="#FF3B3B"
    )
    add_button.pack(pady=(5, 10), fill="x")


    def next_action():
        selected_tracks = [track for track, data in checkboxes.items() if data["var"].get()]
        print(f"Selected Tracks: {selected_tracks} by {artist} on {album} at {timestamp}")
        close_menu()

    def close_menu():
        overlay.destroy()

    next_button = tk.Button(
        popup, text="Next", command=next_action, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#FF3B3B"
    )
    next_button.pack(pady=(20, 5), fill="x")

    exit_button = tk.Button(
        popup, text="Close", command=close_menu, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#D1170D"
    )
    exit_button.pack(fill="x")

def album_submit(album_name, artist_name, timestamp, api_token, root):
    global session_key
    result = get_tracklist(album_name, artist_name, API_KEY, api_token, session_key)
    
    if result[0] == 0:  # Successful album validation
        session_key = result[1]
        tracks = result[2]
        show_track_menu(tracks, root, artist_name, album_name, timestamp)
    else:
        session_key = result[1]
        tk.messagebox.showerror("Error", "Album not found or invalid.")
        

def get_timestamp(date_entry, time_entry):
    datetime_str = f"{date_entry} {time_entry}"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.strptime(datetime_str, datetime_format)
    unix_timestamp = int(dt_object.timestamp()) 
    return unix_timestamp


def create_home_screen():
    # Initialize the main window
    root = tk.Tk()
    root.title("Mac LastFm Scrobbler")
    
    for widget in root.winfo_children():
        widget.destroy()
    
    
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
        command=lambda: album_submit(album_name_entry.get(), artist_name_entry.get(), get_timestamp(timestamp_entry.get_date(), f"{hour_spinbox.get()}:{minute_spinbox.get()}:{second_spinbox.get()}"), api_token, root)
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
        command=lambda: scrobble_track(track_name_entry.get(), track_album_name_entry.get(), track_artist_name_entry.get(), api_token)
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





