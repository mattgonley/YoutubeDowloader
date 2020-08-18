"""
:author: Matt Gonley
:date: May 19, 2020
:description:  file for taking playlist url and downloading the youtube videos on it
"""
import os
import re
import time

from mutagen.mp4 import MP4
from pytube import YouTube  # pytube3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def correctLink(site):  # makes sure link is http(s) so can download
    if 'http' not in site:
        site = "https://" + site
    return site


def scrollToBottom(driver):
    # Currently set for 2 seconds, if internet is slow, one should increase it
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = driver.execute_script("return document.getElementsByTagName('HTML')[0].outerHTML.length;")
    new_height = -100
    while last_height != new_height:
        # Scroll down to bottom
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        last_height = new_height
        new_height = driver.execute_script("return document.getElementsByTagName('HTML')[0].outerHTML.length;")
    hrefs = driver.find_elements_by_tag_name("a")
    return hrefs


def links(browser):
    hrefs = scrollToBottom(browser)
    vids = []  # list to old urls of videos
    prev = []  # variable to ensure link is not a duplicate
    for link in hrefs:
        lin = link.get_property("href")  # get the href value, which has the portion of link
        # watch so only video links will be valid
        if 'watch' in lin:
            lin = lin.split("&list")[0]
            if lin not in prev:  # ensures its a video, not just a link, and not a duplicate
                vids.append(lin)  # appends the obtained link to the full youtube link
                prev.append(lin)  # prevents the duplicate links from being proccessed
    browser.close()
    return vids


def Playlist(path, vids, title):
    errors = ""
    title = re.sub("[^-0-9a-zA-Z_{} ]", '_', title)  # parse out characters that are terrible naming conventions or
    # produce errors
    if path == "":  # no path selected
        path = os.path.dirname(os.path.realpath(__file__)) + "\\music\\" + title  # create folder named after playlist
        print(path)
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    i = 1
    errorList = []
    for vid in vids:  # the list of url's
        try:
            video = YouTube(vid)  # gets the stream type of audio and best quality
            download(path, str(i) + " " + video.title, video)
            print(vid)
        except:
            error = ("The %sth video, failed to download. URL: %s\n\n" %
                     (i, vid))  # link that failed to download
            errors = errors + error
            print(error)
        i = i + 1
    return errors


def single(path, vid):
    error = ""
    if path == "":  # no path selected
        path = os.path.dirname(os.path.realpath(__file__)) + "\\music\\"  # make folder in current working directory
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
    try:
        video = YouTube(vid)  # gets the stream type of audio and best quality
        download(path, video.title, video)
    except:
        error = ("Failed to download video. URL: %s\n" % vid)  # link that failed to download
    return error


# function to download the video and add title/artist
def download(path, name, video):
    name = re.sub('[^a-zA-Z0-9!{}+-]', '_', name)  # parse out characters that are terrible naming conventions
    options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
    # downloads the file to folder, prepends it with playlist number
    options.download(path, skip_existing=True, filename=name, )
    name = path + "/" + name + ".mp4"
    song = MP4(name)
    song["\xa9nam"] = video.title  # video title
    song["\xa9ART"] = video.author  # video author (channel video came from)
    song.save()  # save changes to video
