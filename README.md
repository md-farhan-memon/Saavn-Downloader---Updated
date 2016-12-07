Saavn Downloader
====
This is a downloader which i coded when i discovered a loophole in Saavn Android App (a popular music streaming app) which can be used to download any music from Saavn in mp3 format, AFAIK only Pro users can download songs but that are also DRM protected (i will tell you how broken that is), but with this any user can bypass all these protection and get DRM free music on their disk.

I sent a total of 3 mails i suppose to their only email id that i could possibly find from their website and app - "feedback@saavn.com", along with the PoC but in return i got no reply, which shows that they don't check their mails, God bless those customers, or they don't believe me.

On 30th October 2016 i sent them my first mail and till the date of writing (6th December 2016) i didn't receive any mail from Saavn, so i thought to do a full disclosure along with PoC.

Analysis
====
Let me quicky take you through the process of how i did it.

* I used Burpsuite to perform Man-In-The-Middle attack to see what was really going to and from the app.
* I could see the app was receiving the encrypted urls to the songs so i became sure that decryption has to be done at the app side.
* With a quick look at the decompiled smali files and with 'grep' i could figure out that it was using DES with ECB with no IVs.
* Then it was matter of few minutes that i had a working python script which could download songs without any protection and limit.

DRM Protection Analysis
====
DRM protection used in the app is good but its not well integrated in the app.

AES-256 in CBC mode (I may be wrong) is used for DRM and is implemented in both pure Java and in a NDK library.

I don't know much of NDK reversing but from smali files i could figure out that it uses NDK library if its "available" else it uses the Java method.

And there's the catch, the app tries to load the NDK library but if its not found then it doesn't complain rather it uses the java method.

I think it uses NDK library for performance boost but i couldn't extract more information from it so i used the java method, in java method the encryption key used to decrypt the downloaded songs is again hardcoded in the app, which is not at all secure.

So a user with a Pro account can simply delete the NDK library from the apk, reinstall it and then download songs. Then he can decrypt all those downloaded songs and play it in any of his favourite player.

Prerequisite
====
You need Python and BeautifulSoup4 installed for the script to work.

I used python3 but you can use python2, just make changes in the print statements if you know how to or use python3.

Python3			- https://www.python.org/download/releases/3.0/
BeautifulSoup4	- https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Usage
====
<pre>python3 saavn_downloader.py</pre>

When asked for the song url enter the url of the album from the saavn website eg. http://www.saavn.com/s/album/blah-blah


Final Note
====
This project is show that how small coding and implementation mistakes could lead to big problem.

Some ways to fix these:

* Perform link decryption at server side and not at client side.
* Don't hardcode encryption or decryption keys at the client side.

And another suggestion, keep an eye on those mails you might get something interesting in it :D

Disclaimer
====
This is for education purposes. I should not be held responsible for misusage of the script or damage caused because of it. Use it at your own risk.
