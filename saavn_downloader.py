#!/usr/bin/python3
#coded by Arun Kumar Shreevastave - 10 Sep 2015

from bs4 import BeautifulSoup
import os
import requests
from json import JSONDecoder
import base64

from pyDes import *

proxy_ip = ''
#set http_proxy from environment
if('http_proxy' in os.environ):
    proxy_ip = os.environ['http_proxy']

proxies = {
  'http': proxy_ip,
  'https': proxy_ip,
}
#proxy setup end here

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}
base_url = 'http://h.saavncdn.com'
json_decoder = JSONDecoder()
des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)


input_url = input('Enter the song url:').strip()

try:
    res = requests.get(input_url, proxies=proxies, headers=headers)
except Exception as e:
    print('Error accesssing website error: '+e)
    sys.exit()


soup = BeautifulSoup(res.text,"lxml")
songs_json = soup.find_all('div',{'class':'hide song-json'})

for song in songs_json:
    obj = json_decoder.decode(song.text)
    print(obj['album'],'-',obj['title'])
    enc_url = base64.b64decode(obj['url'].strip())
    dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
    print(dec_url)
    dec_url = base_url + dec_url.replace('mp3:audios','') + '.mp3'
    print(dec_url,'\n')
