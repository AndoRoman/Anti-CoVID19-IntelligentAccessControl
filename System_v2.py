import Lights  # MODULE OF LIGHTS
from Alertas import Voice  # MODULE OF VOICE
import Dect_Image  # MODULE OF AI MASK
import Motors  # MODULE OF MOTORS
import TempC  # MODULE OF TEMPERATURE
import SOAPClient  # Cliente SOAP
import Contador

import RPi.GPIO as GPIO
#############
import threading
import time

###GPIO###
SensorIR = 4
SensorSalida2 = 9
SensorSalida1 = 11
SensorEntrada = 10
BtnPanico = 12
# SensorTemperatura = 2 y 3
# MotorEntrada = 21(DIR), 20(STEP)
# MotorSalida = 13(DIR), 19(STEP)
# LuzVerde = 27
# LuzRoja = 17
# luzAmarilla = 22

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(SensorIR, GPIO.IN)  # sensor IR
GPIO.setup(SensorSalida1, GPIO.IN)
GPIO.setup(SensorSalida2, GPIO.IN)
GPIO.setup(SensorEntrada, GPIO.IN)
GPIO.setup(BtnPanico, GPIO.IN)


####CLASS TO THREAD###
class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        # Function that THREAD will do

        while True:
            i = 0
            # SENSORES IR SALIDA
            if GPIO.input(SensorSalida1) and i == 0 and Contador.CanExitPerson():
                Motors.Open_Barrier_OUT()
                t1 = time.time()
                a = 1
                i += 1
                print("SALIDA #0 ACTIVADA\n")
                time.sleep(3)
                while a != 0:
                    t2 = time.time()
                    if GPIO.input(SensorSalida2):
                        print("SALIDA #1 ACTIVADA\n")
                        Contador.DeletePerson()
                        time.sleep(3)
                        a = 0
                        Motors.Close_Barrier_OUT()

                    if t2 - t1 > 5:
                        print("CERRANDO..., time agotado\n")
                        a = 0
                        Motors.Close_Barrier_OUT()


def BotonPanico():
    if not GPIO.input(BtnPanico):
        Motors.Open_Barrier_OUT()
        Motors.Open_Barrier_IN()
        Voice.speak1("BotonPanico.mp3")

        while not GPIO.input(BtnPanico):
            Lights.Turn_ON_Full()
            time.sleep(2)
            Lights.Turn_OFF_Full()

        Motors.Close_Barrier_IN()
        Motors.Close_Barrier_OUT()


# Create Thread's
threadExit = myThread(1, "Salida")
threadExit.start()

# Variable
acces = False
tempe = 0.0


def __main__():
    SOAPClient.InitializationSystem()
    print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
    Voice.speak1('bienvenido.mp3')

    global acces, tempe
    while True:

        BotonPanico()

        if not GPIO.input(SensorIR):

            print('[INFO] Cliente Recibido...\n [INFO] Evaluando Cliente...')

            if Contador.StatusLocalCapacity():

                # SENSOR DE TEMPERATURA

                tempe = TempC.ReadSensorTemp()
                if tempe > 50.0:
                    print("[INFO] TEMPERATURA: " + str(tempe))
                    Voice.speak1("ErrorTemperatura.mp3")
                else:

                    if tempe < 39.0:
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
                        Voice.speak1("ErrorCamara.mp3")
                        token = False

                    print('[INFO] Evaluacion Concluida...\n [INFO] Enviando Resultandos...')

                    if result == 'Mask' and token and TempSafe:
                        Lights.Turn_ON_Green()
                        Voice.speak1('aceptado.mp3')
                        Motors.Open_Barrier_IN()
                        # OPEN DOOR
                        T = True
                        t1 = time.time()
                        while T:
                            t2 = time.time()
                            if GPIO.input(SensorEntrada):
                                Contador.Person(Temp=tempe, Mask=True, Entry=True)
                                print("ENTRADA...Cantidad de personas: " + str(Contador.Conteo))
                                time.sleep(3)
                                T = False
                                if not Contador.StatusLocalCapacity():
                                    Lights.Turn_ON_Full()
                                    Voice.speak1('MaxCapacidad.mp3')

                            if (t2 - t1) > 5:
                                T = False
                                print("[INFO] Tiempo Agotado...Cerrando Entrada")
                        Lights.Turn_OFF_Green()
                        Motors.Close_Barrier_IN()
                        print('[INFO] Acceso Permitido...\n[INFO] Esperando Nuevo Cliente...')

                    elif (result == 'No Mask' or not TempSafe) and token:

                        Lights.Turn_ON_Red()
                        Voice.speak1('denegado.mp3')
                        print('[INFO] Acceso Denegado...\n[INFO] Esperando Nuevo Cliente...')
                        Contador.Person(Temp=tempe, Mask=False, Entry=False)
                        Lights.Turn_OFF_Red()

                    if not token:
                        print('[INFO] Intentelo de Nuevo...')
                        try:
                            Voice.speak1('error.mp3')
                        except Exception as e:
                            print('[INFO] ¡ERROR DE CONEXIÓN!')

            elif not Contador.StatusLocalCapacity():

                # Pero el contador no puede llegar al max
                Lights.Turn_ON_Full()
                Voice.speak1('localFull.mp3')
                print('[INFO] Local Lleno...\n[INFO] No se permiten Nuevos Clientes...')


if __name__ == '__main__':
    __main__()
    threadExit.join()
