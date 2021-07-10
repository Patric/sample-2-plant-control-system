import json

class Config:
    def __init__(self, jsonConfig):
        jsonPID = json.dumps(jsonConfig)['pid']
        self.__isEnabled = jsonPID['isEnabled']
        self.__ki = jsonPID['ki']
        self.__kp = jsonPID['kp']
        self.__kd = jsonPID['kd']
        self.__SP = jsonPID['SP']
        self.__output_limit_min = jsonPID['output_limit_min']
        self.__output_limit_max = jsonPID['output_limit_max']
        self.__gpio_bcm_out = jsonPID['gpio_bcm_out']
        self.__gpio_pwm_frequency = jsonPID['gpio_pwm_frequency']
        
    def getKi(self):
        