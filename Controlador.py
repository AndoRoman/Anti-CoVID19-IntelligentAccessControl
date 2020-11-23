import sys
import os
import System_v2
import Voice
import time
import RPi.GPIO as GPIO

#EXECUTABLE
try:

    System_v2.__main__()

except Exception:
    Voice.speak1("reiniciodeSistema.mp3")
    time.sleep(30)
    GPIO.cleanup()
    os.execv(sys.executable, ['python'] + sys.argv)
