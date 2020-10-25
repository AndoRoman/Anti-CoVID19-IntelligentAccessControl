
import Lights  # MODULE OF LIGHTS
from Alertas import Voice  # MODULE OF VOICE
import Dect_Image  # MODULE OF AI MASK
import Motors  # MODULE OF MOTORS
import SensorActivate  # MODULE OF TEMPERATURE

import RPi.GPIO as GPIO
#############
import threading
import time

#####VARIABLES###########
Contador = 0
MaxCapacidad = 2  # Max people into building
PersonisExiting = False  # Indicate if a person stay on the door

###GPIO###
SensorIR = 4
SensorSalida2 = 10
SensorSalida1 = 9
SensorEntrada = 11
# SensorTemperatura = 2 y 3
# MotorEntrada = 20(DIR), 21(STEP)
# MotorSalida = 19(DIR), 26(STEP)
# LuzVerde = 27
# LuzRoja = 17
# luzAmarilla = 22


GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(SensorIR, GPIO.IN)  # sensor IR


####CLASS TO THREAD###
class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        ##Function that THREAD will do
        global Contador
        global PersonisExiting
        while (1):

            if (self.name == 'Salida'):
                if not GPIO.input(SensorSalida2):
                    if Contador > 0 and PersonisExiting:

                        Contador -= 1
                        print("SALIDA.. Cantidad de personas: " + str(Contador))
                        Lights.Turn_OFF_Full()
                        time.sleep(1)

                        while (not GPIO.input(SensorSalida2)):
                            time.sleep(2)

                        Motors.Close_Barrier_OUT()
                        PersonisExiting = False

                if not GPIO.input(SensorSalida1):
                    PersonisExiting = True
                    Motors.Open_Barrier_OUT()

            if self.name == 'Entrada':
                if (not GPIO.input(SensorEntrada)):
                    if (Contador < MaxCapacidad):
                        Contador += 1
                        print("ENTRADA...Cantidad de personas: " + str(Contador))
                        time.sleep(1)
                        if (GPIO.input(SensorEntrada)):
                            Motors.Close_Barrier_IN()

                        if (Contador == MaxCapacidad):
                            Lights.Turn_ON_Full()
                            Voice.speak1('MaxCapacidad.mp3')



##Create Thread's######
threadEntrace = myThread(1, "Entrada")
threadExit = myThread(2, "Salida")
threadEntrace.start()  # Inicialization Thread
threadExit.start()


def __main__():
    # Voice.crearVoice()
    print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
    Voice.speak1('bienvenido.mp3')
    while (True):


        if (not GPIO.input(SensorIR)):
            acces = True
            print('[INFO] Cliente Recibido...\n [INFO] Evaluando Cliente...')

            if (Contador < MaxCapacidad and acces):

                # SENSOR DE TEMPERATURA
                if (SensorActivate.ReadSensorTemp() < 36.5):
                    TempSafe = True
                else:
                    TempSafe = False

                try:
                    # RECONOCIMIENTO FACIAL

                    result = Dect_Image.Reconocimiento()
                    token = True
                except Exception as e:
                    print('[INFO] ¡Error de Reconocimiento Facial!')
                    token = False

                print('[INFO] Evaluacion Concluida...\n [INFO] Enviando Resultandos...')


                if (result == 'Mask' and token and TempSafe):
                    Lights.Turn_ON_Green()
                    Voice.speak1('aceptado.mp3')
                    print('[INFO] Acceso Permitido...\n[INFO] Esperando Nuevo Cliente...')
                    # OPEN DOOR
                    Motors.Open_Barrier_IN()
                    Lights.Turn_OFF_Green()

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
    threadEntrace.join()
    threadExit.join()
