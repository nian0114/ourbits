# coding=utf-8
import requests
from config import *

def login():
    with requests.Session() as s:
        r = s.post(ourBitsUrl+"takelogin.php", data={'username': username, 'password': password})
        print(r.headers)
        t = s.get(ourBitsUrl+"torrents.php")
        print(t.text)
        print(t.headers)   