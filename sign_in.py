import http.client
from dotenv import load_dotenv
import webbrowser

def sign_in_handler(api_token):
    conn = http.client.HTTPConnection("www.last.fm")
    payload = ''
    conn.request("GET", "/api/auth/?api_key=f420bcc7f74b33e83f851c8eef8f1f3c&token=ER19zc6n49v_2Z2yjaF0tFy_GUqzzZj", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))