# Group Project
## Description
System monitorujący na bazie komputera Raspberry Pi
## Requirements
**Device**: Raspberry Pi 3B

**Components**:
- High-Precision AD/DA Board
- AM2302 sensor (connections: + to 3V3, - to GND, OUT to GPIO4)
- 3.5inch RPi LCD (A)

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
LCD setup
> https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)

Changing display resolution to 480x320
> https://forums.raspberrypi.com/viewtopic.php?t=5851

Calibrate the touch screen
> https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)

## Usage
Running the application
```
python3 main.py [options]
```
Options:
- --debug-border - show box borders
- --full-screen - open in full screen mode