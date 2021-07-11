import json
import RPi.GPIO as GPIO

class Lamps:
    __pwm = None
    __dc_max = 100
    __dc_min = 0
    __cur_dc = __dc_min
    
    def setConfig(self, jsonConfig):
        jsonLAMPS = jsonConfig['lamps']
        self.__gpio_bcm_out = jsonLAMPS['gpio_bcm_out']
        self.__gpio_pwm_frequency = jsonLAMPS['gpio_pwm_frequency']
            # Mode BCM, GPIO10
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_bcm_out, GPIO.OUT)
        self.__pwm = GPIO.PWM(self.__gpio_bcm_out, self.__gpio_pwm_frequency)
        dc = 0
        self.__pwm.start(dc)
        if jsonLAMPS["is_enabled"] == 1:
            self.turnOnLamps()
        elif jsonLAMPS["is_enabled"] == 0:
            self.turnOffLamps()
        
        
    def turnOnLamps(self):
        self.__cur_dc = self.__dc_max
        self.__pwm.ChangeDutyCycle(self.__cur_dc)
        
    def turnOffLamps(self):
        self.__cur_dc = self.__dc_min
        self.__pwm.ChangeDutyCycle(self.__cur_dc)
    
    def getState(self):
        return self.__cur_dc
        
    def stopLamps(self):
        self.__pwm.stop()
        GPIO.cleanup()
