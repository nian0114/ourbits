# coding=utf-8
import requests
from config import *
from bs4 import BeautifulSoup

def login():
    with requests.Session() as s:
        r = s.post(ourBitsUrl+"takelogin.php", data={'username': username, 'password': password})
        print(r.headers)
        return s

s=login()
t = s.get(ourBitsUrl+"torrents.php")

soup = BeautifulSoup(t.text, 'html.parser')
soup_result = soup.find_all(class_="sticky_top")

for tr in soup_result:
    if 'Free' in str(tr.contents[3]):
        print(tr)

