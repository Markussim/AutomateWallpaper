#/bin/sh
echo "Sudo is required to install libaries."
sudo apt install python3-pip -y
sudo -H pip3 install -r requirements.txt
(crontab -l 2>/dev/null; echo "* * * * * python3 $PWD/main.py $PWD >/dev/null 2>&1") | crontab -
echo "Everything is up and running!"