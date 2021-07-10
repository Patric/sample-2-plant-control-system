from adafruit_seesaw.seesaw import Seesaw
import Sensor

class SoilSensor(Sensor.Sensor):
    
    def __init__(self):
        super().__init__(self.tryInit, "SeaSAW Soil Sensor")

    def tryInit(self):
        i2c = Sensor.busio.I2C(Sensor.board.SCL, Sensor.board.SDA, frequency=100000)
        self.__ss = Seesaw(i2c, addr=0x36)
        
    def getValues(self):
        output = []
        ss_moisture = str(self.__ss.moisture_read())
        output.append({'ss_moisture': ss_moisture, 'unit' : ''})
        ss_temp = str(self.__ss.get_temp())
        output.append({'ss_temp': ss_temp, 'unit':'celsius'})
        print(output)
        return output