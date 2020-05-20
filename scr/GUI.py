import tkinter as tk
from tkinter import filedialog
from scr.download import *
from PIL import ImageTk,Image
import ctypes

def Url():
    link = playlist.get()
    playlist.delete(0,'end')
    message(message)
    text = requests.get(link).text
    link = correctlink(link)
    if 'playlist' in link:
        title = BeautifulSoup(text,"html.parser").title.string
        vid = correctlink(link)
        errors = download(folderPath.get(), vid, title)
    else:
        errors = single(folderPath.get(), link)
    if errors != "":
        message.delete("1.0", 'end')
        message.insert(tk.END, "\n" + errors, 'center')
    else:
        if 'watch' in link:
            message.insert(tk.END, "\n\n Your video has finished downloading", 'center')
        else:
            message.insert(tk.END, "\n\n Your videos have finished downloading", 'center')

def loc():
    global foldePath
    filename = filedialog.askdirectory()
    folderPath.set(filename)

def messText(message):
    message.delete("1.0",'end')
    message.insert(tk.END, "\nThe entry box is for the URL. It will download up to 100 videos for playlists.\n\n"
                           "Link should be for a video, or a playlist.", 'center')

monitor = ctypes.windll.user32
height, width = round(monitor.GetSystemMetrics(1)*.8), round(monitor.GetSystemMetrics(0)*.8)
dis = str(width) +'x'+str(height)
window = tk.Tk(className=' Youtube Downloader')
folderPath = tk.StringVar()
folderPath.set("")
browse = tk.Button(window, text='Select Download Location', width=25, command=loc)
button = tk.Button(window, text='Download', width=25, command=Url)
window.geometry(dis)
window.config(bg='black')
canvas = tk.Canvas(window, width=width, height=250, highlightthickness=0, bg='black')
canvas.pack()
playlist = tk.Entry(window, justify='center')
canvas.create_window(width/2, 200, window=playlist, height=30, width=700)
img = ImageTk.PhotoImage(Image.open('new-youtube-logo.jpg'))
canvas.create_image(width/4, 0, anchor='nw', image=img)
message = tk.Text(window,height=102,width=200, bg='black',fg='white',bd=0, font=("Helvetica",12))
message.tag_configure('center',justify="center")
message.tag_add("center", "1.0", "end")
messText(message)
button.pack()
browse.pack()
message.pack()
window.mainloop()
