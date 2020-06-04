import gpiozero
from time import sleep


###Function to Turn On the signal for denegation the access
def Turn_On_Red():
    LED("GPIO14").on()
    sleep(4)
    LED("GPIO14").off()
###Function to Turn On/Off the signal to indicate that the local is full
def Turn_On_FULL():
    LED("GPIO15").toggle()
###Function to Tun On/Off the signal to indicate that the person can access
def Turn_On_Green():
    LED("GPIO16").toggle()
    sleep(3)
