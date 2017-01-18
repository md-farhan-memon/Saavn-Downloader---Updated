#!/usr/bin/python3
# coded by Arun Kumar Shreevastave - 25 Oct 2016
# Modified by Md. Farhan Memon - 18 Jan 2017

from bs4 import BeautifulSoup
import os
import requests
from json import JSONDecoder
import base64
import wget
import sys
import eyed3
import eyed3.id3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

from pyDes import *

proxy_ip = ''
# set http_proxy from environment
if('http_proxy' in os.environ):
    proxy_ip = os.environ['http_proxy']

proxies = {
  'http': proxy_ip,
  'https': proxy_ip,
}
# proxy setup end here

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}
base_url = 'http://h.saavncdn.com'
json_decoder = JSONDecoder()

# Key and IV are coded in plaintext in the app when decompiled
# and its preety insecure to decrypt urls to the mp3 at the client side
# these operations should be performed at the server side.
des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)

# Taking multiple album URLs from arguments and ignoring index 0 (filename)
albums = sys.argv[1:]

# Creating albums folder and changing the directory
if not os.path.exists('albums'):
    os.makedirs('albums')
    os.chdir('albums')
for  album in albums:

    try:
        res = requests.get(album, proxies=proxies, headers=headers)
    except Exception as e:
        print('Error accesssing website error: '+e)
        sys.exit()

    soup = BeautifulSoup(res.text,"lxml")

    # Encrypted url to the mp3 are stored in the webpage
    songs_json = soup.find_all('div',{'class':'hide song-json'})

    for song in songs_json:
        obj = json_decoder.decode(song.text)
        print(obj['album'],'-',obj['title'])
        enc_url = base64.b64decode(obj['url'].strip())
        dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
        dec_url = base_url + dec_url.replace('mp3:audios','') + '.mp3'
        print(dec_url,'\n')
        album = obj['album']
        if not os.path.exists(album):
                os.makedirs(album)

        path = os.path.join(obj['album'], obj['title'] +'.mp3')
        img_path = os.path.join(obj['album'], obj['title'] +'.jpg')

        filename = wget.download(dec_url,out=path)

        # Downloading cover image
        cover_name = wget.download(obj['image_url'], out=img_path)

        # Adding few tags
        audiofile = eyed3.load(filename)
        if audiofile.tag is None:
            audiofile.tag = eyed3.id3.Tag()
            audiofile.tag.file_info = eyed3.id3.FileInfo(filename)
        audiofile.tag.album = obj['album']
        audiofile.tag.album_artist = obj['singers']
        audiofile.tag.title = obj['title']
        audiofile.tag.save()

        # Adding cover image to audiofile and deleting the image
        audio = MP3(filename, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open(img_path).read()
            )
        )
        audio.save()
        os.remove(cover_name)