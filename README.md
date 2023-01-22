# Group Project
## Description
System monitorujący na bazie komputera Raspberry Pi
## Requirements
**Device**: Raspberry Pi 3B

**Components**:
- High-Precision AD/DA Board
- AM2302 sensor (connections: + to 3V3, - to GND, OUT to GPIO4)

**Operating system**: Raspberry Pi OS with desktop 32-bit

## Setup
```
sudo apt update
sudo apt upgrade

sudo mkdir /var/lib/sensormanager
sudo chmod -R 777 /var/lib/sensormanager
sudo chmod -R 777 .

pip install -r requirements.txt
```

## Usage
Running the application
```
python3 main.py [options]
```
Options:
- --debug-border - show box borders
- --full-screen - open in full screen mode