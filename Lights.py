import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now

RED = 22
GREEN = 17
FULL = 27

GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(RED, GPIO.OUT, initial=GPIO.HIGH) #Red Light
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.HIGH) #Green Light
GPIO.setup(FULL, GPIO.OUT, initial=GPIO.HIGH) #Local FULL Light

def Turn_ON_Red():
    #GPIO.output(17, HIGH) #<--HIGH Only Work with LEDS
    GPIO.output(RED, GPIO.OUT)  #<-- Relay need OUT(turn on) & IN(turn off)
    

def Turn_OFF_Red():
    GPIO.output(RED, GPIO.IN)
    


def Turn_ON_Green():
    #if GPIO.input(27): #<- Read state of GPIO
        #GPIO.output(27, LOW)
    GPIO.output(GREEN, GPIO.OUT)

    
def Turn_OFF_Green():
    GPIO.output(GREEN, GPIO.IN)


def Turn_ON_Full():
    GPIO.output(FULL, GPIO.OUT) #<- Relay
    
def Turn_OFF_Full():
    GPIO.output(FULL, GPIO.IN)


##TEST
def __main__():
    while(True):
        Turn_OFF_Red()
        sleep(1)
        Turn_ON_Red()
        sleep(1)
        Turn_OFF_Red()
        Turn_ON_Full()
        sleep(1)
        Turn_OFF_Full()
        Turn_ON_Green()
        sleep(1)
        Turn_OFF_Green()

if __name__ == '__main__':
    __main__()

