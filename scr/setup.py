from distutils.core import setup

setup(name = 'Youtube Downloader',
      version = '1.0',
      description = 'Download videos from youtube playlist',
      author = 'Matt Gonley',
      url = 'https://github.com/mattgonley/YoutubeDowloader',
      packages = ['Youtube_Downloader'],
      install_requires = ['pytube3',
                          'beautifulsoup4',
                          'tkinter'])