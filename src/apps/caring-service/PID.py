import json
from simple_pid import PID as pid
import RPi.GPIO as GPIO

class PID:
    __pwm = None
    
    def setConfig(self, jsonConfig):
        jsonPID = jsonConfig['pid']
        jsonGPIO = jsonConfig['gpio']
        self.__kp = jsonPID['kp']
        self.__ki = jsonPID['ki']
        self.__kd = jsonPID['kd']
        self.__SP = jsonPID['SP']
        self.__output_limit_min = jsonPID['output_limit_min']
        self.__output_limit_max = jsonPID['output_limit_max']
        
        # kp ki kd
        self.__pid = pid(self.__ki, self.__ki, self.__kd, setpoint=self.__SP)
        pid.output_limits = (self.__output_limit_min, self.__output_limit_max)

        if not self.__pwm:
            self.__gpio_bcm_out = jsonGPIO['gpio_bcm_out']
            self.__gpio_pwm_frequency = jsonGPIO['gpio_pwm_frequency']
            
            # Mode BCM, GPIO10
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__gpio_bcm_out, GPIO.OUT)
        
            self.__pwm = GPIO.PWM(self.__gpio_bcm_out, self.__gpio_pwm_frequency)
            dc = 0
            self.__pwm.start(dc)
        
    def calculateAndExecute(self, input):
        # PID
        self.__PV = input
        self.__CV = self.__pid(self.__PV)
        if self.__CV < 0:
            self.__CV = 0
        print("[PID CV]: " + str(self.__CV))
        print("[PID PV]: " + str(self.__PV))
        print("[PID SP]: " + str(self.__SP))
        self.__pwm.ChangeDutyCycle(self.__CV)

        
    def stopPID(self):
        self.__pwm.stop()
        GPIO.cleanup()