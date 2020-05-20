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

def correctlink(site):
    if 'http' not in site:
        site = "https://" + site
    return site


def links(site):
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

    return vids

def download(path,vids,title):
    errors = ""
    if path == "": # no path selected
        o_s = platform.system() # check OS to allow for linux and windows. May work for mac, i do not know
        # makes the folder with name of playlist inside folder named music. Created where this file is located
        if o_s == "Windows":
            path = os.getcwd() + "\\music\\" + title
        else:
            path = os.getcwd() + "/music/" + title
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    i = 1;
    for vid in vids: # the list of url's
        print(vid)
        try:
            video = YouTube(vid)# gets the stream type of audio and best quality
        except:
            error = ("The %sth video failed to download : %s\n" % (i, vid)) # link that failed to download
            errors=errors+error
            print(error)
        options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
        # downloads the file to folder, prepends it with playlist number
        options.download(path, skip_existing=True, filename_prefix=str(i) + " ")
        i = i + 1
    return errors

def single(path, vid):
    error = ""
    if path == "":  # no path selected
        o_s = platform.system()  # check OS to allow for linux and windows. May work for mac, i do not know
        # makes the folder with name of playlist inside folder named music. Created where this file is located
        if o_s == "Windows":
            path = os.getcwd() + "\\music\\"
        else:
            path = os.getcwd() + "/music/"
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    print(vid)
    try:
        video = YouTube(vid)  # gets the stream type of audio and best quality
    except:
        error = ("The video failed to download : "+ vid)  # link that failed to download
        print(error)

    options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
    # downloads the file to folder, prepends it with playlist number
    options.download(path, skip_existing=True)
    return error