from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 24   # Steps per Revolution (360 / 15)

### Configuration of DriveMotor ####
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['Full'])

step_count = SPR * 2
delay = .0208 / 2
########################################
###OPEN BARRIER
def Open_Barrier():
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)



###CLOSE BARRIER
def Close_Barrier():
    GPIO.output(DIR, CCW)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

##TEST
def __main__():
    print('Abriendo Barrera!')
    Open_Barrier()
    sleep(1)
    print('Cerraron Barrera!')
    Close_Barrier()
    GPIO.cleanup()




if __name__ == '__main__':
    __main__()
