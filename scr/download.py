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

import converter.convert


def correctLink(site):  # makes sure link is http(s) so can download
    if 'http' not in site:
        site = "https://" + site
    return site


def scroll_to_bottom(driver):
    # Currently set for 2 seconds, if internet is slow, one should increase it
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    script = "return document.getElementsByTagName('HTML')[0].outerHTML.length;"
    last_height = driver.execute_script(script)
    new_height = -100
    while last_height != new_height:
        # Scroll down to bottom
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        last_height = new_height
        new_height = driver.execute_script(script)
    hrefs = driver.find_elements_by_tag_name("a")
    return hrefs


def get_playlist_links(browser):
    hrefs = scroll_to_bottom(browser)
    vids = []  # list to old urls of videos
    for href in hrefs:
        lin = href.get_property("href")  # get the href value, which has the portion of link
        # watch so only video links will be valid
        if 'watch' in lin:  # ensures specific link is a video
            lin = lin.split("&list")[0]  # removes playlist index portion
            if lin not in vids:  # ensures its is not a duplicate
                vids.append(lin)  # appends the obtained link to the full youtube link
    browser.close()  # closes browser after all links have been obtained
    return vids


def Playlist(path, vids, title):
    errors = ""
    title = regex(title)
    # produce errors
    path = make_dir(path, title)
    i = 0
    for vid in vids:  # the list of url's
        i += 1
        try:
            vid_download(path, vid, str(i) + " ")
        except:
            error = ("The %sth video, failed to download. URL: %s\n\n" %
                     (i, vid))  # link that failed to download
            errors = errors + error
            print(error)
    converter.convert.search_dir(path)
    return errors


def make_dir(path, title):  # make music directory is no directory is chosen
    if path == "":  # no path selected
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "music", title)  # make folder in current working directory
        try:
            os.makedirs(path)
        except OSError:
            print("Error creating directory, may already exist")
            print("Failed Directory: " + path)
    return path


def vid_download(path, vid, title):
    try:
        video = YouTube(vid)
        name = title + video.title
        return file_attributes(path, name, video)
    except:
        video = YouTube(vid)
        file_attributes(path, title + video.title, video)


def single(path, vid):
    error = ""
    path = make_dir(path, "")
    try:
        name = vid_download(path, vid, "")
        converter.convert.convert_file(name)
    except KeyError:
        error = ("Failed to download video. URL: %s\n" % vid)  # link that failed to download
    return error


# format folder/title string
def regex(string):
    string = string.replace("'", "")
    string = re.sub('[^a-zA-Z0-9!{}+-]', '_', string)  # parse out characters that are terrible naming conventions
    string = re.sub("_+", "_", string)
    if string.endswith("_"):
        string = string[:-1]
    return string


# function to download the video and add title/artist
def file_attributes(path, name, video):
    name = regex(name)
    options = video.streams.filter(type="audio", file_extension="mp4").order_by("bitrate").first()
    # downloads the file to folder, prepends it with playlist number
    name = name.replace("_.mp4", ".mp4")
    options.download(path, skip_existing=True, filename=name, )
    name = os.path.join(path, name + ".mp4")
    song = MP4(name)
    song["\xa9nam"] = video.title  # video title
    song["\xa9ART"] = video.author  # video author (channel video came from)
    song["\xa9alb"] = os.path.basename(os.path.dirname(name))
    song.save()  # save changes to video
    return name


def commandLineArgs(link, path):
    if 'playlist' in link:
        browser = webdriver.Firefox()
        browser.get(link)
        title = browser.execute_script("return document.title;")
        Playlist(path, get_playlist_links(browser), title)
        print("Your videos have finished downloading")
    else:
        single(path, link)
        print("Your video has finished downloading")
