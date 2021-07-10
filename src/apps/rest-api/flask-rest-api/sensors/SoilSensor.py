from adafruit_seesaw.seesaw import Seesaw
from . import Sensor

class SoilSensor(Sensor.SensorInterface):
    __name = "SeaSAW Soil Sensor"
    
    def __init__(self):
        super().__init__(self.tryInit, self.__name)

    def tryInit(self):
        i2c = Sensor.busio.I2C(Sensor.board.SCL, Sensor.board.SDA, frequency=100000)
        self.__ss = Seesaw(i2c, addr=0x36)
    
    def __getValues(self):
        ss_moisture = str(self.__ss.moisture_read())
        ss_temp = str(self.__ss.get_temp())
        output = {'soilSensor': {
            'moisture': {'value': ss_moisture, 'unit': ''},
            'temperature': {'value': ss_temp, 'unit': 'celsius'}},
                  'name': self.__name}
        return output
    
    def getValues(self):
        return super().tryGetValues(self.__getValues)

       