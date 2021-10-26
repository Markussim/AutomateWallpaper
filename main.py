#!/usr/bin/env python3
import os
import requests
import platform
import pathlib
import sys
import json
from PIL import Image
from os.path import exists

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


redditData = requests.get(f'https://www.reddit.com/r/{combinedSubs}/top.json?t={config["timeframe"]}&limit=100', headers = {'User-agent': 'AutomateWallpaper'})

redditJSON = redditData.json()["data"]["children"]
index = 0

previousImagesFile = open(f"{str(pathlib.Path().resolve())}/title.txt", "r")
previousImages = previousImagesFile.read()
previousImagesFile.close()
previousImages = previousImages.split("\n")

while True:
    imageURL = redditJSON[index]["data"]["url"]
    
    imageUsed = False
    for previousImage in previousImages:
        if previousImage == imageURL:
            imageUsed = True

    if imageUsed: 
        index += 1
        continue

    if imageURL[-4:] == ".jpg":
        image = requests.get(imageURL, allow_redirects=True)
        open('tmp.jpg', 'wb').write(image.content)
        img = Image.open("tmp.jpg")
        img.close()
        if img.width >= 1920 and img.height >= 1080:
            lastLinkFile = open(f"{str(pathlib.Path().resolve())}/lastLink.txt", "r")
            previousFile = lastLinkFile.read()
            previousImagesFile.close()

            if not exists("wallpaper.jpg"):
                open('wallpaper.jpg', 'w').write("Test")

            if previousFile != redditJSON[index]["data"]["url"]:
                os.remove("wallpaper.jpg")
                os.rename("tmp.jpg", "wallpaper.jpg")

            open(f"{str(pathlib.Path().resolve())}/lastLink.txt", "w").write(redditJSON[index]["data"]["url"])
            open('title.txt', 'a').write(imageURL + "\n")
            break
    index += 1

#Keep track of max number of images to reserve memory
for i in range(len(previousImages) - config["rememberedImages"]):
    with open('title.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('title.txt', 'w') as fout:
        fout.writelines(data[1:])

print(redditData.headers["x-ratelimit-remaining"])
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{str(pathlib.Path().resolve())}\\wallpaper.jpg" , 0)
else:
    os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {str(pathlib.Path().resolve())}/wallpaper.jpg")
    