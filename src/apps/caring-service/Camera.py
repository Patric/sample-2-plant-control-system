from picamera import PiCamera

class Camera:
    __i = 0
    def __init__(self):
        self.__camera = PiCamera()
        self.__camera.resolution = (1920, 1080)
        self.__camera.start_preview()
        
    def savePhoto(self, location):
        self.__camera.capture(f"{location}/photo{self.__i}.jpg")
        self.__i += 1
        if self.__i >= 0: self.__i = 0

    def stopCapture(self):
        self.__camera.stop_preview()