import tkinter as tk
from scrobble_menus import show_save_scrobble_menu

#Menu that shows all of the tracks either fetched by the Last.fm api OR fetched from the file about an album
def show_track_menu(tracks, root, artist, album, timestamp, increment, api_key, api_token, session_key):
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
    scrollbar_y = tk.Scrollbar(track_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set)
    
    #Used for easy scrolling
    def on_mouse_wheel(event):
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")  
        else:
            canvas.yview_scroll(1, "units")
    def on_mouse_wheel_horizontal(event):
        if event.delta > 0: 
            canvas.xview_scroll(-1, "units")
        else:  
            canvas.xview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Shift-MouseWheel>", on_mouse_wheel_horizontal)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    checkboxes = {}  # Define checkboxes after creating track checkboxes

    #If a checkbox changes
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

    #To add a track to the list
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

            var.trace_add("write", lambda *args: track_selection_changed())

    #Remove a track from the list
    def remove_track(track):
        if track in checkboxes:
            checkboxes[track]["row_frame"].destroy()
            del checkboxes[track]
            
    select_all_var = tk.BooleanVar()

    #Select all tracks from the list using the checkbox
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
        show_save_scrobble_menu(root, selected_tracks, artist, album, timestamp, increment, api_key, api_token, session_key)

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