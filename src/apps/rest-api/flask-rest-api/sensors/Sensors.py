import json
from sensors.SoilSensor import SoilSensor
from sensors.TempMCP9808Sensor import TempMCP9808Sensor
from sensors.LightIntensitySensor import LightIntensitySensor
from sensors.SGP30AirQualitySensor import SGP30AirQualitySensor
from sensors.BME280Sensor import BME280Sensor

class Sensors:
    
    def __init__(self):
        try:
            self.__initSensors()
        except Exception as exception:
            print("Unexpected exception: " + str(exception))
            
    def __initSensors(self):
        self.__lightIntensitySensor = LightIntensitySensor()
        self.__gasSensor = SGP30AirQualitySensor()
        self.__temperatureSensor = TempMCP9808Sensor()
        self.__soilMoistureAndTempSensor = SoilSensor()
        self.__humidityPressureTemperatureSensor = BME280Sensor()
    
    def getValues(self):
        output = [self.__lightIntensitySensor.getValues(),
                                   self.__gasSensor.getValues(),
                                   self.__temperatureSensor.getValues(),
                                   self.__soilMoistureAndTempSensor.getValues(),
                                   self.__humidityPressureTemperatureSensor.getValues()]
        print(output)
        return output