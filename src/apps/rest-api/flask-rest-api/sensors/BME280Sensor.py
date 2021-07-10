from adafruit_bme280 import basic as adafruit_bme280
from . import Sensor


class BME280Sensor(Sensor.SensorInterface):
    __name = "Humidity, Pressure and Temperature BME280 Sensor"
    
    def __init__(self):
        super().__init__(self.tryInit, self.__name)
        
    def tryInit(self):
        self.__i2c = Sensor.board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.__i2c)
        
    def __getValues(self):
        temperature = self.__bme280.temperature
        humidity = self.__bme280.humidity
        pressure = self.__bme280.pressure
        output = {'bmeSensor': {
            'temperature': {'value': temperature, 'unit': 'celsius'},
            'humidity': {'value': humidity, 'unit': '%'},
            'pressure': {'value': pressure, 'unit': 'hPa'}},
                  'name': self.__name}
        return output
    
    def getValues(self):
        return super().tryGetValues(self.__getValues)