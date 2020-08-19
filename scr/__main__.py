"""
:author: Matt Gonley
:date: August 18, 2020
"""

import argparse
import sys
import os


if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # Reference:
    major = sys.version_info[0]

    python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2])
    if major != 3:
        print("YoutubeDownloader requires Python 3\nYou are using Python %s, which is not supported" % python_version)
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--directory", nargs="?", dest="path", default="", help="path to download file", )
    parser.add_argument(nargs="*", dest="links", help="Links to youtube", )
    args = parser.parse_args()
    if len(sys.argv) == 1:
        import scr.gui
        scr.gui.main()
    else:
        import scr.download
        if args.path is not "" and not os.path.exists(args.path):
            print("The specified download directory is invalid")
            sys.exit(1)
        for arg in args.links:
            scr.download.commandLineArgs(arg, args.path)
