#/bin/sh
(crontab -l 2>/dev/null; echo "* * * * * python3 $PWD/main.py $PWD >/home/markus/pucko/pucko.txt 2>&1") | crontab -
