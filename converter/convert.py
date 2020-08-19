import argparse

from moviepy.editor import *


def convert_file(file_path):
    mp3_file = file_path.replace(".mp4", ".mp3")
    if not os.path.isfile(mp3_file):
        clip = AudioFileClip(file_path)
        clip.write_audiofile(mp3_file)
        clip.close()


def search_dir(directory):
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                search_dir(os.path.join(directory, file))
            elif file.endswith(".mp4"):
                convert_file(os.path.join(directory, file))
    elif os.path.isfile(directory) and directory.endswith(".mp4"):
        convert_file(directory)
    else:
        print("Dir: [" + directory + "] is an invalid directory or file. Please ensure you had the file path correct,"
                                     " and if so, that it pointed to a directory or mp4 file.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-rel', "--rel", nargs="*", dest="rel_path", default=[], help="Take relative paths", )
    parser.add_argument(nargs="*", dest="abs_path", help="Example path to mp4 file", )

    args = parser.parse_args()
    for rel_path in args.rel_path:
        search_dir(os.path.join(__file__, rel_path))
    for abs_path in args.abs_path:
        search_dir(abs_path)
