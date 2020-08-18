import re
import subprocess
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
os.system("pip install -r requirements.txt")
output = subprocess.Popen("pip show pytube3", shell=True, stdout=subprocess.PIPE)
location = str(output.stdout.read())
location = location.split("Location: ")[1]
location = location.split("Requires: ")[0]
location = location.replace("\\r\\n", "")
location = location + "\\pytube\\"

file = location+"extract.py"

with open(file, "r+") as f:
    data = f.read()
    f.seek(0)
    f.write(re.sub(r"formats\[i\]\[\"cipher",
                   "formats[i][\"signatureCipher", data))
    f.truncate()
    f.close()

