from subprocess import Popen, PIPE
import time

def ReadSensorTemp():
    temp = Popen("sudo ./sensor", shell=True, stdout=PIPE).stdout
    return float(temp.read())


