import smbus
from . import Sensor

class LightIntensitySensor(Sensor.SensorInterface):
    
    __name = "ISL29125 light intensity sensor"
    
    def __init__(self):
        super().__init__(self.tryInit, self.__name)

    def tryInit(self):
        self.__bus = smbus.SMBus(1)
        # ISL29125 address, 0x44(68)
        # Select configuation-1register, 0x01(01)
        #               0x0D(13)        Operation: RGB, Range: 10000 lux, Res: 16 Bits
        self.__bus.write_byte_data(0x44, 0x01, 0x0D)

    def __getValues(self):
        data = self.__bus.read_i2c_block_data(0x44, 0x09, 6)
        green = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        blue = data[5] * 256 + data[4]
        output = ({'RGB':
                   {'r': f"{red}",
                    'g': f"{green}",
                    'b':f"{blue}"},
                   'unit':'lux',
                   'name':self.__name})
        return output
        
    def getValues(self):
        return super().tryGetValues(self.__getValues)