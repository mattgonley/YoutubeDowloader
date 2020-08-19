"""
:author: Matt Gonley
:date: May 19, 2020
:description:  Interactive GUI for downloader
"""

import ctypes
import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk, Image

from .download import *

playlist = tk.Entry
folderPath = ""
message = tk.Text


def Url():
    link = playlist.get()
    playlist.delete(0, 'end')
    link = correctLink(link)
    browser = webdriver.Firefox()
    try:
        browser.get(link)
    except:
        messText(message, "\n The URL you entered is did not work. Please enter a valid link,\n\n"
                          "or if you believe is should have, try it again.\nURL: " + link)
        return
    messText(message, "") # removes message from the gui
    if 'playlist' in link:
        title = browser.execute_script("return document.title;")
        errors = Playlist(folderPath, get_playlist_links(browser), title)
        finished = "\n\n Your videos have finished downloading"
    else:
        errors = single(folderPath, link)
        finished = "\n\n Your video has finished downloading"
    if errors != "":
        messText(message, errors)
    else:
        message.insert(tk.END, finished, 'center')


def dir_loc():
    global folderPath
    filename = filedialog.askdirectory()
    folderPath = filename


def messText(mess, st):  # creates inital message for user (instructions/info)
    mess.delete("1.0", 'end')
    if st == "":
        mess.insert(tk.END, "\nThe entry box is for the URL.\n\n"
                            "Link should be for a video or a YouTube playlist.", 'center')
    else:
        mess.insert(tk.END, st + '\n', 'center')


def main():
    global message, playlist, folderPath
    # gets the display and sets size of window based upon that
    monitor = ctypes.windll.user32
    height, width = round(monitor.GetSystemMetrics(1) * .8), round(monitor.GetSystemMetrics(0) * .8)
    dis = str(width) + 'x' + str(height)

    window = tk.Tk(className=' Youtube Downloader')  # create window
    folderPath = ""
    browse = tk.Button(window, text='Select Download Location', width=25, command=dir_loc)  # create browse button
    button = tk.Button(window, text='Download', width=25, command=Url)  # create submit button
    window.geometry(dis)  # sets window size
    window.config(bg='black')  # sets background black
    canvas = tk.Canvas(window, width=width, height=250, highlightthickness=0,
                       bg='black')  # adds canvas for youtube logo
    canvas.pack()
    playlist = tk.Entry(window, justify='center')
    canvas.create_window(width / 2, 200, window=playlist, height=30, width=700)
    img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'new-youtube-logo.jpg')))
    canvas.create_image(width / 4, 0, anchor='nw', image=img)
    message = tk.Text(window, height=102, width=200, bg='black', fg='white', bd=0,
                      font=("Helvetica", 12))  # font settings for text
    message.tag_configure('center', justify="center")  # centers the message
    message.tag_add("center", "1.0", "end")
    messText(message, "")
    button.pack()
    browse.pack()
    message.pack()
    window.mainloop()
