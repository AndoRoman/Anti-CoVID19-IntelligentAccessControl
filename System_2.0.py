import Lights  # MODULE OF LIGHTS
from Alertas import Voice  # MODULE OF VOICE
import Dect_Image  # MODULE OF AI MASK
import Motors  # MODULE OF MOTORS
import TempC  # MODULE OF TEMPERATURE

import RPi.GPIO as GPIO
#############
import threading
import time

#####VARIABLES###########
global Contador
Contador = 0
MaxCapacidad = 2  # Max people into building
PersonisExiting = False  # Indicate if a person stay on the door

###GPIO###
SensorIR = 4
SensorSalida2 = 9
SensorSalida1 = 11
SensorEntrada = 10
BotonPanico = 12
# SensorTemperatura = 2 y 3
# MotorEntrada = 21(DIR), 20(STEP)
# MotorSalida = 13(DIR), 19(STEP)
# LuzVerde = 27
# LuzRoja = 17
# luzAmarilla = 22
# BOTON PANICO = 12

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(SensorIR, GPIO.IN)  # sensor IR
GPIO.setup(SensorSalida1, GPIO.IN)
GPIO.setup(SensorSalida2, GPIO.IN)
GPIO.setup(SensorEntrada, GPIO.IN)
GPIO.setup(BotonPanico, GPIO.IN)


####CLASS TO THREAD###
class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        ##Function that THREAD will do
        
        while (1):
            i = 0
            if (self.name == 'Salida'):
                if (GPIO.input(SensorSalida1) and i == 0 and Contador > 0):
                    Motors.Open_Barrier_OUT()
                    t1 = time.time()
                    a = 1
                    i += 1
                    print("SALIDA #0 ACTIVADA\n")
                    time.sleep(3)
                    while (a != 0):
                        t2 = time.time()
                        if (GPIO.input(SensorSalida2)):
                            print("SALIDA #1 ACTIVADA\n")
                            Contador -= 1
                            time.sleep(3)
                            a = 0
                            Motors.Close_Barrier_OUT()

                        if t2 - t1 > 5:
                            print("CERRANDO..., time agotado\n")
                            a = 0
                            Motors.Close_Barrier_OUT()

            



def Entrada():
    if (GPIO.input(SensorEntrada)):
        Contador += 1
        print("ENTRADA...Cantidad de personas: " + str(Contador))
        time.sleep(3)
        if (Contador == MaxCapacidad):
            Lights.Turn_ON_Full()
            Voice.speak1('MaxCapacidad.mp3')

        return True

    return False


##Create Thread's######
# threadEntrace = myThread(1, "Entrada")
threadExit = myThread(1, "Salida")
# threadEntrace.start()  # Inicialization Thread
threadExit.start()


def __main__():
    # Voice.crearVoice()
    print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
    Voice.speak1('bienvenido.mp3')
    while (True):
        
        #BOTON PANICO
#        if not GPIO.input(BotonPanico):
#                Motors.Open_Barrier_OUT()
#                Motors.Open_Barrier_IN()
#                
#                while GPIO.input(BotonPanico):
#                    Lights.Turn_ON_Full()
#                    time.sleep(1)
#                    Lights.Turn_OFF_Full()
                    

        if (not GPIO.input(SensorIR)):
            acces = True
            print('[INFO] Cliente Recibido...\n [INFO] Evaluando Cliente...')

            if (Contador < MaxCapacidad and acces):

                # SENSOR DE TEMPERATURA
                tempe = TempC.ReadSensorTemp()
                print("[INFO] TEMPERATURA: " + str(tempe))
                if (tempe < 40.0):
                    TempSafe = True
                else:
                    TempSafe = False

                try:
                    # RECONOCIMIENTO FACIAL
                    time.sleep(0.5)
                    result = Dect_Image.Reconocimiento()
                    token = True
                except Exception as e:
                    print('[INFO] ¡Error de Reconocimiento Facial!')
                    token = False

                print('[INFO] Evaluacion Concluida...\n [INFO] Enviando Resultandos...')

                if (result == 'Mask' and token and TempSafe):
                    Lights.Turn_ON_Green()
                    Voice.speak1('aceptado.mp3')
                    Motors.Open_Barrier_IN()
                    # OPEN DOOR
                    T = True
                    t1 = time.time()
                    while (T):
                        t2 = time.time()
                        if (GPIO.input(SensorEntrada)):
                            Contador += 1
                            print("ENTRADA...Cantidad de personas: " + str(Contador))
                            time.sleep(3)
                            T = False
                            if (Contador == MaxCapacidad):
                                Lights.Turn_ON_Full()
                                Voice.speak1('MaxCapacidad.mp3')

                                               

                        if ((t2 - t1) > 5):
                            T = False
                            print("[INFO] Tiempo Agotado...Cerrando Entrada")

                    Lights.Turn_OFF_Green()
                    Motors.Close_Barrier_IN()
                    print('[INFO] Acceso Permitido...\n[INFO] Esperando Nuevo Cliente...')

                elif ((result == 'No Mask' or not TempSafe) and token):

                    Lights.Turn_ON_Red()
                    Voice.speak1('denegado.mp3')
                    print('[INFO] Acceso Denegado...\n[INFO] Esperando Nuevo Cliente...')
                    Lights.Turn_OFF_Red()

                if (not token):
                    print('[INFO] Intentelo de Nuevo...')
                    try:
                        Voice.speak1('error.mp3')
                    except Exception as e:
                        print('[INFO] ¡ERROR DE CONEXIÓN!')


            elif (Contador == MaxCapacidad):

                ## Pero el contador no puede llegar al max
                Lights.Turn_ON_Full()
                Voice.speak1('localFull.mp3')
                print('[INFO] Local Lleno...\n[INFO] No se permiten Nuevos Clientes...')


if __name__ == '__main__':
    __main__()
    threadExit.join()
