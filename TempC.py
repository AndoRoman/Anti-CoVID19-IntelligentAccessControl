from subprocess import Popen, PIPE
import time

def ReadSensorTemp():
    temp = Popen("sudo ./sensor", shell=True, stdout=PIPE).stdout
    return float(temp.read())
while(1):
    print("\n")
    print("Sensor: % 04.2f" %(ReadSensorTemp()))
    time.sleep(2)

