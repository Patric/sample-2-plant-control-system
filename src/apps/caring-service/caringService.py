#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  caringService.py
#  
#  Copyright 2021  <sample.ska.igluna@gmail.com>
#  
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
from Camera import Camera
from Lamps import Lamps

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import os


def checkIfFolderExists(folderName):
    CHECK_FOLDER = os.path.isdir(folderName)
    if not CHECK_FOLDER:
        os.makedirs(folderName)

LOGSDIR = '/home/pi/sample2/src/apps/static/logs'
CONFIG_DIR = '/home/pi/sample2/src/apps/static/config/caring-service'
PHOTO_DIR = '/home/pi/sample2/src/apps/static/images/photo'


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

try:
    automatic_control = PID()
    logger.info("Initiated PID controller." + json.dumps(config))
    automatic_control.setConfig(config)
    logger.info("Loaded config for PID" + json.dumps(config))
except Exception as exc:
    logger.error(exc)

try:
    camera = Camera()
    logger.info("Initiated camera.")
except Exception as exc:
    logger.error(exc)

try:
    lamps = Lamps()
    logger.info("Initiated lamps.")
    lamps.setConfig(config)
    logger.info("Loaded config for lamps" + json.dumps(config))
except Exception as exc:
    logger.error(exc)


def on_config_modified(event):
    print(f"{event.src_path} has been modified")
    try:
        with open(f"{CONFIG_DIR}/config.json") as f:
            config = json.load(f)
 
        automatic_control.setConfig(config)
        logger.info("Loaded config for PID " + json.dumps(config))
        
        lamps.setConfig(config)
        logger.info("Loaded config for lamps " + json.dumps(config))
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
            logger.info(f"[PV]: {pv} [CV]: {cv}, [SP]: {sp} \n {temps}")
        except Exception as exc:
            logger.error(exc)
            
        try:
            camera.savePhoto(PHOTO_DIR)
            logger.info(f"Successfully saved photo to {PHOTO_DIR}")
        except Exception as exc:
            print(str(exc))
            logger.error(exc)
            
        try:
            print(lamps.getState())
            logger.info(f"Lamps state: {lamps.getState()}")
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
    camera.stopCapture()
    lamps.stopLamps()