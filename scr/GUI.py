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


def Url():
    link = playlist.get()
    playlist.delete(0, 'end')
    link = correctLink(link)
    try:
        text = requests.get(link).text
    except:
        messText(message,"\n The URL you entered is did not work. Please enter a valid link,\n\n"
                         "or if you believe is should have, try it again.\nURL: "+link)
        return
    messText(message, "")
    str = ""
    if 'playlist' in link:
        title = bs(text, "html.parser").title.string
        vid = correctLink(link)
        errors = Playlist(folderPath.get(), links(vid), title)
        str = "\n\n Your videos have finished downloading"
    else:
        errors = single(folderPath.get(), link)
        str = "\n\n Your video has finished downloading"
    if errors != "":
        messText(message,errors)
        #message.delete("1.0", 'end')
        #message.insert(tk.END, "\n" + errors, 'center')
    else:
        message.insert(tk.END, str, 'center')


def globe():  # gets selected download location
    global folderPath, message, playlist

def dir_loc():
    filename = filedialog.askdirectory()
    folderPath.set(filename)


def messText(message, st):  # creates inital message for user (instructions/info)
    message.delete("1.0", 'end')
    if st == "":
        message.insert(tk.END, "\nThe entry box is for the URL.\n\n"
                               "Link should be for a video, or a YouTube playlist.", 'center')
    else:
        message.insert(tk.END, st+'\n', 'center')


def main():
    globe()
    # gets the display and sets size of window based upon that
    monitor = ctypes.windll.user32
    height, width = round(monitor.GetSystemMetrics(1) * .8), round(monitor.GetSystemMetrics(0) * .8)
    dis = str(width) + 'x' + str(height)

    window = tk.Tk(className=' Youtube Downloader')  # create window
    folderPath = tk.StringVar()
    folderPath.set("")
    browse = tk.Button(window, text='Select Download Location', width=25, command=dir_loc)  # create browse button
    button = tk.Button(window, text='Download', width=25, command=Url)  # create submit button
    window.geometry(dis)  # sets window size
    window.config(bg='black')  # sets background black
    canvas = tk.Canvas(window, width=width, height=250, highlightthickness=0, bg='black')  # adds canvas for youtube logo
    canvas.pack()
    playlist = tk.Entry(window, justify='center')
    canvas.create_window(width / 2, 200, window=playlist, height=30, width=700)
    img = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__))+'./new-youtube-logo.jpg'))
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