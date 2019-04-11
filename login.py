# coding=utf-8
import requests
from config import *
from bs4 import BeautifulSoup

def login():
    with requests.Session() as s:
        r = s.post(ourBitsUrl+"takelogin.php", data={'username': username, 'password': password})
        print(r.headers)
        return s

def getFreeTorrent(t,class_name):
    soup = BeautifulSoup(t.text, 'html.parser')
    soup_result = soup.find_all(class_=class_name)

    return soup_result

s=login()
t = s.get(ourBitsUrl+"torrents.php")

for tr in getFreeTorrent(t,"sticky_top"):
    if 'Free' in str(tr.contents[3]):
        print(tr)

for tr in getFreeTorrent(t,"sticky_normal"):
    if 'Free' in str(tr.contents[3]):
        print(tr)
