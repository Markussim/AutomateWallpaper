@ECHO OFF
ECHO {"timeframe": "day","rememberedImages": 0}> config.json
COPY NUL title.txt
COPY NUL lastLink.txt
ECHO Successfully created config files!
ECHO Installing python dependencies.
pip3 install -r requirements.txt
ECHO Successfully installed python dependencies!
SCHTASKS /DELETE /TN AutomateWallpaper
SCHTASKS /CREATE /SC MINUTE /TN AutomateWallpaper /TR "'C:\Users\Linus Romland\AppData\Local\Microsoft\WindowsApps\python3.exe' 'C:\Users\Linus Romland\Git\AutomateWallpaper\main.py'"

PAUSE
