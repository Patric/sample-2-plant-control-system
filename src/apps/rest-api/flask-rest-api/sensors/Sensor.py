import json
import board
import busio
from time import sleep
from datetime import datetime
from picamera import PiCamera
import logging

class SensorInterface:
    __name = "unnamed"
    __getValues = "undefined"
    
    def __init__(self, tryInit, sensorName):
        try:
            self.__name = sensorName
            tryInit()
        except Exception as exception:
            self.__status = self.error('Error while initiating sensor', exception)

    def error(self, message, exception):
        output = {'sensorName': self.__name, 'errorMessage': message, 'exception': str(exception)}
        print(output)
        return output
    
    def log(self, message):
        print(message)
    
    def tryGetValues(self, getValues):
        try:
            return getValues()
        except Exception as exception:
            return self.error('Error while reading sensor value', exception)
    
    def getName(self):
        return self.__name;
    
    def tryInit(self):
        raise NotImplementedError()
    
    def getValues(self):
        raise NotImplementedError()