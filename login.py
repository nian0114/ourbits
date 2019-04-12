# coding=utf-8
import requests
import re
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

def getInfo(td):
    soup_result_td = tr.find_all("td")        
    download_id = re.match(r'.*?details.php\?id\=(\d+)(.*)',str(soup_result_td)).group(1)
    size = soup_result_td[9].text
    seeder = soup_result_td[11].text
    
    return download_id, size, seeder

s=login()
t = s.get(ourBitsUrl+"torrents.php")

for tr in getFreeTorrent(t,"sticky_top"):
    if 'Free' in str(tr.contents[3]) and 'hitandrun' not in str(tr.contents[3]):
        download_id, size, seeder=getInfo(tr)
        download_link = "https://ourbits.club/download.php?id=" + download_id + "&passkey=" + passkey + "&https=0"
        print(tr)

for tr in getFreeTorrent(t,"sticky_normal"):
    if 'Free' in str(tr.contents[3]) and 'hitandrun' not in str(tr.contents[3]):
        download_id, size, seeder=getInfo(tr)
        download_link = "https://ourbits.club/download.php?id=" + download_id + "&passkey=" + passkey + "&https=0"        
