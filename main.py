#!/usr/bin/env python3
import os
import requests
import platform
import pathlib
import sys
import json
from PIL import Image

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

config = json.load(open('config.json',))

text_file = open(f"{str(pathlib.Path().resolve())}/subreddits.txt", "r")
rawSubreddits = text_file.read()
text_file.close()

subreddits = rawSubreddits.split("\n")
combinedSubs = ""

for i in range(len(subreddits)):
    combinedSubs += subreddits[i]
    if(i < len(subreddits) -1):
        combinedSubs += "+"


redditData = requests.get(f'https://www.reddit.com/r/{combinedSubs}/top.json?t={config["timeframe"]}', headers = {'User-agent': 'AutomateWallpaper'})

redditJSON = redditData.json()["data"]["children"]
index = 0

while True:
    imageURL = redditJSON[index]["data"]["url"]
    txt = redditJSON[index]["data"]["title"]

    lastTitleFile = open(f"{str(pathlib.Path().resolve())}/title.txt", "r")
    lastTitle = lastTitleFile.read()
    lastTitleFile.close()

    if lastTitle != txt:
        if imageURL[-4:] == ".jpg":
            image = requests.get(imageURL, allow_redirects=True)
            open('tmp.jpg', 'wb').write(image.content)
            img = Image.open("tmp.jpg")
            img.close()
            if img.width >= 1920 and img.height >= 1080:
                os.remove("wallpaper.jpg")
                os.rename("tmp.jpg", "wallpaper.jpg")
                open('title.txt', 'w').write(txt)
                break
        index = index + 1
    else:
        break


# open('wallpaper.jpg', 'wb').write(image.content)

print(redditData.headers["x-ratelimit-remaining"])
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{str(pathlib.Path().resolve())}\\wallpaper.jpg" , 0)
else:
    os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {str(pathlib.Path().resolve())}/wallpaper.jpg")