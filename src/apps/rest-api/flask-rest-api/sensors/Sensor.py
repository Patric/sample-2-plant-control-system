import json
import board
import busio
from time import sleep
from datetime import datetime
from picamera import PiCamera
import logging

class Sensor:
    __name = "unnamed"
    
    def __init__(self, tryInit, sensorName):
        self.__name = sensorName
        try:
            tryInit()
        except Exception as exception:
            self.__status = self.error('Error while initiating sensor', exception)

    def error(self, message, exception):
        output = json.dumps({'sensorName': self.__name, 'errorMessage': message, 'exception': str(exception)})
        print(output)
        return output
    
    def log(self, message):
        print(message)

    def tryInit(self):
        raise NotImplementedError()
    
    def getName(self):
        return self.__name;
