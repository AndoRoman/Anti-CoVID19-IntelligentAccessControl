import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH) #Red Light
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH) #Green Light
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH) #Local FULL Light

def Turn_ON_Red():
    #GPIO.output(17, HIGH) #<--HIGH Only Work with LEDS
    GPIO.output(17, GPIO.OUT)  #<-- Relay need OUT(turn on) & IN(turn off)
    

def Turn_OFF_Red():
    GPIO.output(17, GPIO.IN)
    


def Turn_ON_Green():
    #if GPIO.input(27): #<- Read state of GPIO
        #GPIO.output(27, LOW)
    GPIO.output(27, GPIO.OUT)

    
def Turn_OFF_Green():
    GPIO.output(27, GPIO.IN)


def Turn_ON_Full():
    GPIO.output(22, GPIO.OUT) #<- Relay
    
def Turn_OFF_Full():
    GPIO.output(22, GPIO.IN)

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
