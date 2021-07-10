from SGP30AirQualitySensor import SGP30AirQualitySensor
from SoilSensor import SoilSensor
from TempMCP9808Sensor import TempMCP9808Sensor
from LightIntensitySensor import LightIntensitySensor


print("Im good")

#d ef getValue(self):
#try:
#data = bus.read_i2c_block_data(0x44, 0x09, 6)


LightIntensitySensor().getValues()
soil = SoilSensor()
SGP30AirQualitySensor().getValues()
TempMCP9808Sensor().getValues()
soil.getValues()
