# Instruction for setup
Run on Raspberry Pi 4

## Install Raspbian
Using the Raspberry Pi Imager, simply install Raspbian (32 Bit)

## Clone Git Repository
`sudo git clone https://github.com/phultquist/smart-album-cover`
`cd smart-album-cover`
`sudo git clone https://github.com/phultquist/resize`
`sudo git clone https://github.com/phultquist/mobile`

## Install Requirements
`sudo pip3 install -r requirements.txt`
This will take a while (about 5-10 minutes)

`sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
`sudo python3 -m pip install --force-reinstall adafruit-blinka`

`sudo pip3 install adafruit-circuitpython-tsl2591`

Finally, install schedule
`sudo pip3 install schedule`

## Configure Pi
> Run `sudo raspi-config` on the command line, then use the arrow keys to select 'Interfacing Options' and 'I2C' to tell the RasPi to enable the I2C interface. Then select 'Finish' and reboot the RasPi.

## Run the Program
`sudo python3 run.py auto`
See more in ../README.md. You'll be asked to sign in first