import os
import http.client
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
API_KEY = os.getenv("API_KEY")

def generate_token():
    conn = http.client.HTTPSConnection("ws.audioscrobbler.com")
    
    payload = ''
    headers = {}
    
    conn.request("GET", f"https://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={API_KEY}", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    root = ET.fromstring(data)
    
    token = root.find('token').text
    
    return token