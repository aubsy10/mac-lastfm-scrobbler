import os
import webbrowser
import hashlib
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET

load_dotenv()
API_SECRET = os.getenv("API_SECRET")

def sign_in(api_key, api_token):
    print(f"token: {api_token}")
    auth_url = f"http://www.last.fm/api/auth/?api_key={api_key}&token={api_token}"
    # Open the URL in the default web browser
    webbrowser.open(auth_url)
    return True

def generate_token(api_key):
    url = f"https://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        token = root.find('token').text
        return token
    else:
        # Handle errors (you can log the error or raise an exception)
        print("Error:", response.status_code)
        return None

def get_sig(params):
    concatenated_string = "".join(f"{key}{value}" for key, value in sorted(params.items()))
    string_to_hash = concatenated_string + API_SECRET
    api_sig = hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()
    return api_sig

def get_session_key(api_key, api_token):
    params = {
        "api_key": api_key,
        "method": "auth.getSession",
        "token": api_token
    }
    print(f"Params: {params}")
    api_sig = get_sig(params)
    url = f"https://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key={api_key}&token={api_token}&api_sig={api_sig}"
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        session_key = root.find(".//session/key").text
        return session_key
    else:
        print("Error:", response.status_code)
        return None
    
      

