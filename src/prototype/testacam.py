from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()
# Camera warm-up time
i = 0
while True:
    sleep(2)
    camera.capture(f"foo{i}.jpg")
    i += 1
