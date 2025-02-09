# utils.py
from datetime import datetime
import tkinter as tk

#Utilities specifically relating to the filenames of the tracks and albums for the save data and getting the timestamp in the correct format

CHAR_MAP = {
    "/": "_SLASH_",
    "\\": "_BACKSLASH_",
    ":": "_COLON_",
    "*": "_ASTERISK_",
    "?": "_QUESTION_",
    "\"": "_QUOTE_",
    "<": "_LT_",
    ">": "_GT_",
    "|": "_PIPE_",
    "-": "_DASH_"
}

def encode_filename(text):
    for char, replacement in CHAR_MAP.items():
        text = text.replace(char, replacement)
    return text

def decode_filename(text):
    for char, replacement in CHAR_MAP.items():
        text = text.replace(replacement, char)
    return text

def get_timestamp(date_entry, time_entry):
    datetime_str = f"{date_entry} {time_entry}"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.strptime(datetime_str, datetime_format)
    unix_timestamp = int(dt_object.timestamp()) 
    return unix_timestamp