import adafruit_sgp30
from . import Sensor

class SGP30AirQualitySensor(Sensor.Sensor):
    __name = "SGP30 Air Quality Sensor"

    def __init__(self):
        super().__init__(self.tryInit, self.__name)

    def tryInit(self):
        i2c = Sensor.busio.I2C(Sensor.board.SCL, Sensor.board.SDA, frequency=100000)
        self.__sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        self.__sgp30.iaq_init()
        self.__sgp30.set_iaq_baseline(0x8973, 0x8AAE)

    def getValues(self):
        output = {'gas':
                  {'CO2':{'value': self.__sgp30.eCO2, 'unit':'ppm'},
                   'TVOCppb': {'value': self.__sgp30.TVOC, 'unit':'ppb'}},
                  'name': self.__name}
     
        return output
    