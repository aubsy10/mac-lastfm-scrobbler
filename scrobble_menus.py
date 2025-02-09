import tkinter as tk
from file_handler import save_selected_tracks
from album_scrobble import scrobble_album

#File has code which show the save scrobble menu and the scrobbled menu
#The save scrobble menu asks the user if they'd like to save the tracks in the album to a file for future use
#The scrobbled menu shows users which songs have been scrobbled successfully.

def show_save_scrobble_menu(root, selected_tracks, artist, album, timestamp, increment, api_key, api_token, session_key):
    overlay = tk.Frame(root, bg="#121212")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    popup = tk.Frame(
        overlay, bg="#1E1E1E", padx=30, pady=30, relief="flat",
        borderwidth=5, highlightbackground="#D1170D", highlightthickness=2
    )
    popup.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        popup, text="Save Selected Tracks?", font=("Helvetica", 14, "bold"),
        fg="#FFFFFF", bg="#1E1E1E"
    ).pack(pady=10)

    def save_tracks():
        save_selected_tracks(selected_tracks, artist, album)
        close_menu()
        new_session_key = scrobble_album(selected_tracks, artist, album, timestamp, increment, api_key, api_token, session_key)
        show_scrobbled_menu(root, selected_tracks, artist, album)

    def skip_save():
        close_menu()
        new_session_key = scrobble_album(selected_tracks, artist, album, timestamp, increment, api_key, api_token, session_key)
        show_scrobbled_menu(root, selected_tracks, artist, album, api_key, api_token, session_key)
    
    def close_menu():
        overlay.destroy()

    save_button = tk.Button(
        popup, text="Save", command=save_tracks, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#FF3B3B"
    )
    save_button.pack(pady=(20, 5), fill="x")
    
    skip_button = tk.Button(
        popup, text="Skip", command=skip_save, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#FF3B3B"
    )
    skip_button.pack(pady=(20, 5), fill="x")

    exit_button = tk.Button(
        popup, text="Close", command=close_menu, bg="#FFFFFF", fg="#D1170D",
        font=("Helvetica", 12), relief="flat", padx=10, pady=5, borderwidth=0,
        activebackground="#D1170D"
    )
    exit_button.pack(fill="x")

            
def show_scrobbled_menu(root, selected_tracks, artist, album, api_key, api_token, session_key):
    overlay = tk.Frame(root, bg="#121212")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    popup = tk.Frame(
        overlay, bg="#1E1E1E", padx=30, pady=30, relief="flat",
        borderwidth=5, highlightbackground="#D1170D", highlightthickness=2
    )
    popup.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        popup, text="Scrobbled", font=("Helvetica", 14, "bold"),
        fg="#FFFFFF", bg="#1E1E1E"
    ).pack(pady=10)

    track_list_frame = tk.Frame(popup, bg="#1E1E1E")
    track_list_frame.pack(pady=20, fill="both", expand=True)

    track_list = tk.Listbox(
        track_list_frame, bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12), selectmode=tk.SINGLE,
        activestyle="none", height=8
    )
    track_list.pack(fill="both", expand=True)

    for track in selected_tracks:
        track_list.insert(tk.END, f"{track} - {artist} - {album}")

    def close_popup():
        overlay.destroy()

    close_button = tk.Button(
        popup, text="Close", bg="#D1170D", fg="#FFFFFF", font=("Helvetica", 12),
        command=close_popup
    )
    close_button.pack(pady=10)