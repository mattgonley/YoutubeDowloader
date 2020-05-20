"""
:author: Matt Gonley
:date: May 19, 2020
:description:  file for taking playlist url and downloading the youtube videos on it
"""
import os
import re

import requests
from bs4 import BeautifulSoup
from mutagen.mp4 import MP4
from pytube import YouTube  # pytube3


def correctlink(site):  # makes sure link is http(s) so can download
    if 'http' not in site:
        site = "https://" + site
    return site


def links(site):
    text = requests.get(site).text  # html of the webpage
    soup = BeautifulSoup(text, "html.parser")
    vids = []  # list to old urls of videos
    prev = '   '  # variable to ensure link is not a duplicate
    for link in soup.find_all('a'):
        lin = link.get('href')  # get the href value, which has theportion of link
        # watch so only video links will be valid
        if 'watch' in lin and prev not in lin:  # ensures its a video, not just a link, and not a duplicate
            vids.append("https://www.youtube.com" + lin)  # appends the obtained link to the full youtube link
            prev = lin  # prevents the duplicate links from being proccessed

    return vids


def Playlisy(path, vids, title):
    errors = ""
    title = re.sub('[^-0-9a-zA-Z_\[\]{} ]+', '_', title)  # parse out characters that are terrible naming conventions or
    # produce errors
    print (title)
    if path == "":  # no path selected
        path = os.getcwd() + "/music/" + title  # create folder named after playlist
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    i = 1
    for vid in vids:  # the list of url's
        print(vid)
        cont = True
        try:
            video = YouTube(vid)  # gets the stream type of audio and best quality
        except:
            error = ("The %sth video, failed to download. URL: %s\n" %
                     (i, vid))  # link that failed to download
            errors = str(errors) + str(error)
            print(error)
            cont = False
        if cont:  # download if video was obtained from link
            download(path, str(i) + " " + video.title, video)
        i = i + 1
    return errors


def single(path, vid):
    error = ""
    cont = True
    if path == "":  # no path selected
        path = os.getcwd() + "/music/"  # make folder in current working directory
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    print(vid)
    try:
        video = YouTube(vid)  # gets the stream type of audio and best quality
    except:
        error = ("Failed to download video. URL: %s\n" % vid)  # link that failed to download
        print(error)
        cont = False
    if cont:  # download only if video was valid
        download(path, video.title, video)
    return error


# function to download the video and add title/artist
def download(path, name, video):
    name = re.sub('[^a-zA-Z0-9!{}+-]', '_', name)  # parse out characters that are terrible naming conventions
    options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
    # downloads the file to folder, prepends it with playlist number
    options.download(path, skip_existing=True, filename=name)
    name = path + "/" + name + ".mp4"
    song = MP4(name)
    song["\xa9nam"] = video.title  # video title
    song["\xa9ART"] = video.author  # video author (channel video came from)
    song.save()  # save changes to video
