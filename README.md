## YoutubeDowloader
Python script to download YouTube playlists

## Author
* Matt Gonley

## Details
* Download any size playlist
* downloads as mp4 files with only the audio

## Required Software
This program makes use of selenium webdrivers, and in particular their firefox webdriver.
Fot that to function, a software driver needs to be installed.
It can de downloaded from: github.com/mozilla/geckodriver/releases/latest
When installed, the file needs to be added to the path.


## Installation
**NOTE**: Python 3 is required.
```console
# clone the repo
$ git clone https://github.com/mattgonley/YoutubeDowloader.git

# change the working directory to YoutubeDownloader
$ cd YoutubeDownloader

# install python3 if it is not already installed

# install the requirements
$ python install.py
```

## Usage
```console
$ python -m scr
```

## Features
* Download playlist of any size
* Download single video
* The Song(s) will have artist and title lable
* Choose download location, and make folder with playlist name for songs their

## Intended Features (Potential future features)
* Convert mp4 files to mp3
* Detail number of videos downloaded out of number in playlist
* Allow to download videos behind sensativity filter on youtube

## License
* MIT License 
#
* If their is features one would like added, feel free to comment and its possible I will add it when I have the time
