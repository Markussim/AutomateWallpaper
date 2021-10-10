#/bin/sh
(crontab -l 2>/dev/null; echo "* * * * * python3 $PWD/main.py >/dev/null 2>&1") | crontab -
