#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2021  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import board
import busio
import adafruit_mcp9808
from time import sleep
from picamera import PiCamera
from adafruit_seesaw.seesaw import Seesaw
import adafruit_sgp30
import smbus

# ======================================= Light intensity
# Get I2C bus
bus = smbus.SMBus(1)

# ISL29125 address, 0x44(68)
# Select configuation-1register, 0x01(01)
#               0x0D(13)        Operation: RGB, Range: 10000 lux, Res: 16 Bits
bus.write_byte_data(0x44, 0x01, 0x0D)


# =======================================
camera = PiCamera()
camera.resolution = (1024, 768)
#camera.start_preview()
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
ss = Seesaw(i2c, addr=0x36) 

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)


while True:
    print("[GAS SENSOR] eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
   # print(
   #         "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
   #         % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
   #     )
    mcp = adafruit_mcp9808.MCP9808(i2c)
    print("[TEMP SENSOR]: " + str(mcp.temperature))
    camera.capture('foo.jpg')
    touch = ss.moisture_read()
    temp = ss.get_temp()
    print("[SOIL PROP SENSOR]: TEMP " + str(temp) + "  MOISTURE: " + str(touch))
    
        
    # ISL29125 address, 0x44(68)
    # Read data back from 0x09(9), 6 bytes
    # Green LSB, Green MSB, Red LSB, Red MSB, Blue LSB, Blue MSB
    data = bus.read_i2c_block_data(0x44, 0x09, 6)

    # Convert the data
    green = data[1] * 256 + data[0]
    red = data[3] * 256 + data[2]
    blue = data[5] * 256 + data[4]

    # Output data to the screen
    print(f"[RGB SENSOR] R:{red}, G:{green}, B:{blue} lux ")
    print("____________________________________-")
    sleep(2)
