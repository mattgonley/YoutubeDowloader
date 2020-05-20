import tkinter as tk
from tkinter import filedialog
from scr.download import *
from PIL import ImageTk,Image

def Url():
    link = playlist.get()
    playlist.delete(0,'end')
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

def loc():
    global foldePath
    filename = filedialog.askdirectory()
    folderPath.set(filename)

window = tk.Tk(className=' Youtube Downloader')
folderPath = tk.StringVar()
folderPath.set("")
browse = tk.Button(window, text='Select Download Location', width=25, command=loc)
button = tk.Button(window, text='Download', width=25, command=Url)
window.geometry("1300x700")
window.config(bg='black')
canvas = tk.Canvas(window, width=1000, height=250, highlightthickness=0, bg='black')
canvas.pack()
playlist = tk.Entry(window, justify='center')
canvas.create_window(500, 200, window=playlist, height=30, width=700)
img = ImageTk.PhotoImage(Image.open('new-youtube-logo.jpg'))
canvas.create_image(200, 0, anchor='nw', image=img)
message = tk.Text(window,height=102,width=200, bg='black',fg='white',bd=0, font=("Helvetica",12))
message.tag_configure('center',justify="center")
message.tag_add("center", "1.0", "end")
message.insert(tk.END,"\nThe entry box is for the URL. It will download up to 101 videos for playlists. Link should be\n\n"
                            "for video, or playlist. Enter link in http:// or https:// format", 'center')
button.pack()
browse.pack()
message.pack()
window.mainloop()
