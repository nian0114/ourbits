# coding=utf-8
import requests
import re
from config import *
from bs4 import BeautifulSoup
from pymongo import MongoClient
from qbittorrent import Client

conn = MongoClient(mongo_ip, mongo_port)
db = conn.pt_site
my_set = db.ourbits

qb = Client(system_url)
qb.login()

def delete_permanently_files(infohash):
    r = requests.get(system_url + '/api/v2/torrents/delete?hashes=' + infohash + '&deleteFiles=false')
    
def get_files(status):
    r = requests.get(system_url + '/api/v2/torrents/info?filter='+status+'sort=ratio')
    datas = json.loads(r.text)
    return datas

def getSize(num):
    real_num = float(re.findall("\d+\.?\d*",num)[0])
    if 'GB' in num:
        return real_num*1024*1024*1024
    elif 'MB' in num:
        return real_num*1024*1024
    elif 'TB' in num:
        return real_num*1024*1024*1024*1024

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
    size = getSize(soup_result_td[9].text)
    seeder = soup_result_td[11].text
    
    return download_id, size, seeder

s=login()
t = s.get(ourBitsUrl+"torrents.php")

for tr in getFreeTorrent(t,"sticky_top"):
    if 'Free' in str(tr.contents[3]) and 'hitandrun' not in str(tr.contents[3]):
        download_id, size, seeder=getInfo(tr)
        download_link = "https://ourbits.club/download.php?id=" + download_id + "&passkey=" + passkey + "&https=0"
        result = my_set.find_one({"id":download_id})
        link_list = [download_link]
        if result is None:
            qb.download_from_link(link_list)            
            my_set.insert_one({"id":download_id,"href":download_link,"size":size,"seeder":seeder,"top":1,"deal":0})
        else:
            my_set.update_one({"id":download_id},{"$set":{"seeder":seeder}})

for tr in getFreeTorrent(t,"sticky_normal"):
    if 'Free' in str(tr.contents[3]) and 'hitandrun' not in str(tr.contents[3]):
        download_id, size, seeder=getInfo(tr)
        download_link = "https://ourbits.club/download.php?id=" + download_id + "&passkey=" + passkey + "&https=0"
        result = my_set.find_one({"id":download_id})
        if result is None:
            my_set.insert_one({"id":download_id,"href":download_link,"size":size,"seeder":seeder,"top":0,"deal":0}) 
        else:
            my_set.update_one({"id":download_id},{"$set":{"seeder":seeder}})            
