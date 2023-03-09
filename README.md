# Group Project
## Description
System monitorujący na bazie komputera Raspberry Pi
## Requirements
**Device**: Raspberry Pi 3B

**Components**:
- High-Precision AD/DA Board
- AM2302 sensor (connections: + to 3V3, - to GND, OUT to GPIO12)
- 3.5inch RPi LCD (A)

**Operating system**: Raspberry Pi OS with desktop 32-bit

## Setup
```
sudo apt update
sudo apt upgrade

sudo mkdir /var/lib/sensormanager
sudo chmod -R 777 /var/lib/sensormanager

sudo apt-get install python-dev libatlas-base-dev
pip install -r requirements.txt
```

### Enabling SPI Interface
```
sudo nano /boot/config.txt
```
Choose Interfacing Options -> SPI -> Yes

### LCD setup
Documentation:

> https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)

Installing the driver

```
cd ~
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod +x LCD35-show
./LCD35-show
```


Changing display resolution to 480x320 (optional if wrong resolution)
> https://forums.raspberrypi.com/viewtopic.php?t=5851

Calibrating the touch screen

```
sudo apt-get install xinput-calibrator
```
Click the "Menu" button on the taskbar, choose "Preference" -> "Calibrate Touchscreen".

You may need to reboot the device.

### Autostart
To make this application run at startup create sensormanager.desktop file
```
sudo nano /etc/xdg/autostart/sensormanager.desktop
```

In this file, add the following lines:

```
[Desktop Entry]
Type=Application
Name=SensorManager
Exec=/usr/bin/python3 /path/to/project/main.py --full-screen
```
Reboot
## Usage
Running the application
```
python3 main.py [options]
```
Options:
- --debug-border - show box borders
- --full-screen - open in full screen mode
