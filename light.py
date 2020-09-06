# Simple demo of the TSL2591 sensor.  Will print the detected light value
# every second.
import time
 
import board
import busio
import adafruit_tsl2591
 
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
 
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

def lux():
    return sensor.lux