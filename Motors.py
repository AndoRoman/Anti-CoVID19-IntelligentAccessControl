from time import sleep
import RPi.GPIO as GPIO

DIR_IN = 21  # Direction GPIO Pin
STEP_IN = 20  # Step GPIO Pin
DIR_OUT = 26
STEP_OUT = 19

CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 24  # Steps per Revolution (360 / 15)

### Configuration of DriveMotor ####
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_IN, GPIO.OUT)
GPIO.setup(STEP_IN, GPIO.OUT)
GPIO.setup(STEP_OUT, GPIO.OUT)
GPIO.setup(DIR_OUT, GPIO.OUT)

GPIO.output(DIR_IN, CW)

step_count = SPR * 2
delay = .0208 / 2


########################################

###OPEN BARRIER
def Open_Barrier_IN():
    GPIO.output(DIR_IN, CCW)
    for x in range(step_count):
        GPIO.output(STEP_IN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_IN, GPIO.LOW)
        sleep(delay)


###CLOSE BARRIER
def Close_Barrier_IN():
    GPIO.output(DIR_IN, CW)
    for x in range(step_count):
        GPIO.output(STEP_IN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_IN, GPIO.LOW)
        sleep(delay)


def Open_Barrier_OUT():
    GPIO.output(DIR_OUT, 1)
    for i in range(step_count):
        GPIO.output(STEP_OUT, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_OUT, GPIO.LOW)
        sleep(delay)


def Close_Barrier_OUT():
    GPIO.output(DIR_OUT, 0)
    for i in range(step_count):
        GPIO.output(STEP_OUT, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_OUT, GPIO.LOW)
        sleep(delay)


##TEST
def __main__():
    while True:
        
        print('Abriendo Barrera!')
        Open_Barrier_OUT()
        sleep(1)
        print('Cerraron Barrera!')
        Close_Barrier_OUT()
        sleep(1)



if __name__ == '__main__':
    __main__()
