"""
:author: Matt Gonley
:date: August 18, 2020
"""

import sys

if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # Reference:
    major = sys.version_info[0]

    python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2])
    if major != 3:
        print("YoutubeDownloader requires Python 3\nYou are using Python %s, which is not supported" % (python_version))
        sys.exit(1)

    import scr.gui

    if len(sys.argv) == 1:
        scr.gui.main()
    else:
        import scr.download

        for arg in sys.argv[1:]:
            scr.download.commandLineArgs(arg)
