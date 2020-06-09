import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW) #Red Light
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW) #Green Light
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) #Local FULL Light

def Turn_ON_Red():
    GPIO.output(17, HIGH) #<--HIGH Only Work with LEDS
    #GPIO.output(17, GPIO.OUT)  #<-- Relay need OUT(turn on) & IN(turn off)
    sleep(4)
    #GPIO.output(17, GPIO.IN)
    GPIO.output(17, LOW)

def Turn_ON_Green():
    if GPIO.input(27): #<- Read state of GPIO
        GPIO.output(27, LOW)
        #GPIO.output(27, IN)
    else:
        GPIO.output(27, HIGH) #<--HIGH Only Work with LEDS
        #GPIO.output(27, OUT)


def Turn_ON_Full():
    if GPIO.input(22):
        GPIO.output(22, LOW)
        #GPIO.output(22, IN) #<- Relay
    else:
        GPIO.output(22, HIGH) #<--HIGH Only Work with LEDS
        #GPIO.output(22, OUT)

##TEST
def __main__():
    while(True):
        Turn_ON_Red()
        sleep(1)
        Turn_ON_Green()
        sleep(1)
        Turn_ON_Full()
        
if __name__ == '__main__':
    main()
