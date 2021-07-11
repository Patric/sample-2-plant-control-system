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
from time import sleep
import sys
sys.path.append("/home/pi/sample2/src/apps/rest-api/flask-rest-api/")
from sensors import SoilSensor
from sensors import BME280Sensor
from sensors import TempMCP9808Sensor
import logging
import json
from statistics import mean
from PID import PID

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import os


def checkIfFolderExists(folderName):
    CHECK_FOLDER = os.path.isdir(folderName)
    if not CHECK_FOLDER:
        os.makedirs(folderName)

LOGSDIR = '/home/pi/sample2/src/apps/www-data/logs'
CONFIG_DIR = '/home/pi/sample2/src/apps/www-data/config/caring-service'
checkIfFolderExists(LOGSDIR)
logging.basicConfig(filename=f"{LOGSDIR}/caring_system.log", level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


with open(f"{CONFIG_DIR}/config.json") as f:
    try:
        config = json.load(f)
    except Exception as exc:
        logger.error(" | loading default config |" + str(exc))
        with open(f"{CONFIG_DIR}/defaultConfig.json") as fdefault:
            config = json.load(fdefault)
    
automatic_control = PID()
automatic_control.setConfig(config)
logger.info("Loaded config" + json.dumps(config))

def on_config_modified(event):
    print(f"{event.src_path} has been modified")
    try:
        with open('config.json') as f:
            config = json.load(f)
 
        automatic_control.setConfig(config)
        logger.info("Loaded config" + json.dumps(config))
    except Exception as exc:
        print(exc)
        logger.error(str(exc))


event_handler = PatternMatchingEventHandler(["config.json"], ["*.log"])
event_handler.on_modified = on_config_modified
observer = Observer()
observer.schedule(event_handler, CONFIG_DIR)
observer.start()




print("Sample2 Caring Service started")
try:
    while True:
        #TO:DO refactor
        temps = []
        try:
            temps.append(TempMCP9808Sensor().getValues()['mcpTemperature']['value'])
        except Exception as exc:
            logger.error(exc)
            
        try:
            temps.append(SoilSensor().getValues()['soilSensor']['temperature']['value'])
        except Exception as exc:
            logger.error(exc)
        
        try:
            temps.append(BME280Sensor().getValues()['bmeSensor']['temperature']['value'])
        except Exception as exc:
            logger.error(exc)
        try:   
            pv, cv, sp = automatic_control.calculateAndExecute(mean(temps))
            logger.info(f"[PV]: {pv} [CV]: {cv}, [SP]: {sp}")
        except Exception as exc:
            print(str(exc))
            logger.error(exc)
            
        print(temps)
        sleep(2)
except Exception as exception:
    print(exception)
    logger.error(exception)
finally:
    automatic_control.stopPID()
    observer.stop()
    observer.join()