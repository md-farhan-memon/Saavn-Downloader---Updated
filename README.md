Saavn Downloader
====

This is a the modified/updated version of already existing PoC which can be found here: https://github.com/arunKumarNOP/Saavn-Downloader

I came accross this script and surprisingly it was working, so thought of adding few features for easy, organized and improved download. Quick list of added features.

* Downloading multiple albums/playlists at a time
* Added tags like title, album and artist to the song to organise in the music player
* Added cover imaged to the audio file for recognition in the music player

Prerequisite
====
Besides Python and BeautifulSoup4, I used other libraries too which needs to be installed for the script to work.

Python3     - https://www.python.org/download/releases/3.0/

BeautifulSoup4  - https://www.crummy.com/software/BeautifulSoup/bs4/doc/

eyeD3           - http://eyed3.nicfit.net/

Mutagen         - https://pypi.python.org/pypi/mutagen

Each of them can be pip installed easily.

Usage
====
<pre>python saavn_downloader.py http://www.saavn.com/s/album/blah-blah1 http://www.saavn.com/s/album/blah-blah2 http://www.saavn.com/s/album/blah-blah3...</pre>

Final Note & Disclaimer
====

This is for education purposes. I should not be held responsible for misusage of the script or damage caused because of it. Use it at your own risk.