from subprocess import Popen, PIPE
import time

def ReadSensorTemp():
    temp = Popen("sudo ./sensor", shell=True, stdout=PIPE).stdout
    return float(temp.read())


def __main__():
    while(True):
        print("TEMPERATURA: " + str(ReadSensorTemp()))
        time.sleep(2)
        
