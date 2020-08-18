"""
Sherlock: Find Usernames Across Social Networks Module
This module contains the main logic to search for usernames at social
networks.
"""

import sys


if __name__ == "__main__":
    # Checking if the user is using the correct version of Python
    # Reference:
    major = sys.version_info[0]

    python_version = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])
    if major != 3:
        print("YoutubeDonwloader requires Python 3\nYou are using Python %s, which is not supported" % (python_version))
        sys.exit(1)

    import scr.GUI
    scr.GUI.main()