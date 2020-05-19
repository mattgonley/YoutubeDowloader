"""
:author: Matt Gonley
:date: May 19, 2020
:description:  file for taking playlist url and downloading the youtube videos on it
"""
from bs4 import BeautifulSoup
import requests
import os
from pytube import YouTube #pytube3
import platform

site = input("URL needs to be in http:// or https:// format \n"
             "Youtube playlist link, max number of videos in playlist 100 :\n")
text = requests.get(site).text # html of the webpage
soup = BeautifulSoup(text,"html.parser")
vids = [] # list to old urls of videos
prev = '   ' # variable to ensure link is not a duplicate
for link in soup.find_all('a'):
    lin = link.get('href') # get the href value, which has theportion of link
    # watch so only video links will be valid
    if 'watch' in lin and prev not in lin: # ensures its a video, not just a link, and not a duplicate
        vids.append("https://www.youtube.com" + lin) # appends the obtained link to the full youtube link
        prev = lin # prevents the duplicate links from being proccessed
o_s = platform.system() # check OS to allow for linux and windows. May work for mac, i do not know
# makes the folder with name of playlist inside folder named music. Created where this file is located
if o_s == "Windows":
    path = os.getcwd() + "\\music\\" + soup.title.string
else:
    path = os.getcwd() + "/music/" + soup.title.string
try:
    os.makedirs(path)
except OSError:
    print("Error creating directory, may already exist")
i = 1;
for vid in vids: # the list of url's
    try:
        video = YouTube(vid)
        # gets the stream type of audio and best quality
        options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
        # downloads the file to folder, prepends it with playlist number
        options.download(path, skip_existing=True, filename_prefix=str(i)+" ")
    except:
        print(vid + ' failed to download') # link that failed to download
    i = i +1


