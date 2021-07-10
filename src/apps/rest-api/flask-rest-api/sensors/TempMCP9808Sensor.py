import adafruit_mcp9808
import Sensor

class TempMCP9808Sensor(Sensor.Sensor):

    
    def __init__(self):
        super().__init__(self.tryInit, "MCP9808 temperature sensor")
        
    def tryInit(self):
        self.__i2c = Sensor.busio.I2C(Sensor.board.SCL, Sensor.board.SDA, frequency=100000)
        self.__mcp= adafruit_mcp9808.MCP9808(self.__i2c)
        
    def getValues(self):
        mcp_temp = adafruit_mcp9808.MCP9808(self.__i2c).temperature
        output = {'mcp_temp': mcp_temp}
        print(output)
        return output