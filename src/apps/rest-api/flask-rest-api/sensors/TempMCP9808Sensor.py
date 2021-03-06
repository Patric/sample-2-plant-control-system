import adafruit_mcp9808
from . import Sensor

class TempMCP9808Sensor(Sensor.SensorInterface):
    __name = "MCP9808 temperature sensor"
    
    def __init__(self):
        super().__init__(self.tryInit, self.__name)
        
    def tryInit(self):
        self.__i2c = Sensor.busio.I2C(Sensor.board.SCL, Sensor.board.SDA, frequency=100000)
        self.__mcp= adafruit_mcp9808.MCP9808(self.__i2c)
        
    def __getValues(self):
        mcp_temp = adafruit_mcp9808.MCP9808(self.__i2c).temperature
        output = {'mcpTemperature': {
                    'value': mcp_temp,
                    'unit': 'celsius'},
                  'name': self.__name}
        return output
    
    def getValues(self):
        return super().tryGetValues(self.__getValues)