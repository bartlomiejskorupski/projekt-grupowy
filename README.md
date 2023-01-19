# Group Project
## Description
...

## Requirements
Update Python to version 3.11
```
cd ~/Downloads
wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz
tar -zxvf Python-3.11.1.tgz
cd Python-3.11.1
./configure --enable-optimizations
sudo make altinstall
cd /usr/bin
sudo rm python
sudo ln -s /usr/local/bin/python3.11 python
```
## Setup

```
pip install -r requirements.txt
```

Add root privilages
```
sudo chmod -R 777 .
sudo chmod -R 777 /var/lib/groupproject/
```

## Usage
TODO: ADD FLAGS
...
```
python3 ./main.py
```