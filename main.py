#!/usr/bin/env python3
import os
import requests
import pathlib

text_file = open(f"{str(pathlib.Path().resolve())}/subreddits.txt", "r")
rawSubreddits = text_file.read()
text_file.close()

subreddits = rawSubreddits.split("\n")
combinedSubs = ""

for i in range(len(subreddits)):
    combinedSubs += subreddits[i]
    if(i < len(subreddits) -1):
        combinedSubs += "+"


redditData = requests.get(f'https://www.reddit.com/r/{combinedSubs}/top.json', headers = {'User-agent': 'AutomateWallpaper'})

redditJSON = redditData.json()["data"]["children"]
index = 0

while True:
    imageURL = redditJSON[index]["data"]["url"]
    if imageURL[-4:] == ".jpg":
        break
    index = index + 1

image = requests.get(imageURL, allow_redirects=True)
open('wallpaper.jpg', 'wb').write(image.content)

print(redditData.headers["x-ratelimit-remaining"])
os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {str(pathlib.Path().resolve())}/wallpaper.jpg")

