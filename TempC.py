from subprocess import Popen, PIPE

def ReadSensorTemp():
    temp = Popen("sudo ./sensor", shell=True, stdout=PIPE).stdout
    return float(temp.read())

print("Sensor: % 04.2f" %(ReadSensorTemp()))
