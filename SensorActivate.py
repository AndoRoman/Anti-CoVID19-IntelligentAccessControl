# Libreria ctypes permite la compatibilidad de data en C
from ctypes import *

libsensorTemp = CDLL('./TEMP.so')  # Cargar Libreria en C

libsensorTemp.objectTemp.argTypes = (c_int,)

libsensorTemp.objectTemp.restype = c_double  # Definir el tipo del retorno de la funcion


def ReadSensorTemp():
    return libsensorTemp.objectTemp()


print("Sensor: " + str(ReadSensorTemp()))
