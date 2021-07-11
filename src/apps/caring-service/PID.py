import json
from simple_pid import PID as pid
import RPi.GPIO as GPIO

class PID:
    __pwm = None
    __CV = 0
    __previousModeManual = False
    
    def setConfig(self, jsonConfig):
        jsonPID = jsonConfig['pid']
        jsonHEATER = jsonConfig['heater']
        self.__manual = jsonPID['manual']
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
            self.__gpio_bcm_out = jsonHEATER['gpio_bcm_out']
            self.__gpio_pwm_frequency = jsonHEATER['gpio_pwm_frequency']
            
            # Mode BCM, GPIO10
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__gpio_bcm_out, GPIO.OUT)
        
            self.__pwm = GPIO.PWM(self.__gpio_bcm_out, self.__gpio_pwm_frequency)
            dc = 0
            self.__pwm.start(dc)
        if self.__manual == 1:
            self.__pid.set_auto_mode(False, last_output=self.__CV)
            self.__CV = jsonPID['CV']
            self.__previousModeManual = True
        elif self.__manual == 0 and self.__previousModeManual:
            self.__pid.set_auto_mode(True, last_output=self.__CV)
            self.__previousModeManual = False
        
    def calculateAndExecute(self, input):
        # PID
        if self.__manual != 1:
            self.__PV = input
            self.__CV = self.__pid(self.__PV)
            if self.__CV < 0:
                self.__CV = 0
            print("[PID PV]: " + str(self.__PV))
        print("[PID CV]: " + str(self.__CV))
        print("[PID SP]: " + str(self.__SP))
        self.__pwm.ChangeDutyCycle(self.__CV)
        return self.__PV, self.__CV, self.__SP

        
    def stopPID(self):
        self.__pwm.stop()
        GPIO.cleanup()