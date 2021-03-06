import datetime

import Lights  # MODULE OF LIGHTS
from Alertas import Voice  # MODULE OF VOICE
import Dect_Image  # MODULE OF AI MASK
import Motors  # MODULE OF MOTORS
import TempC  # MODULE OF TEMPERATURE
import SOAPClient  # Cliente SOAP
import Contador
import QRreader
import RPi.GPIO as GPIO
#############
import threading
import time

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

# Variable
acces = False
tempe = 0.0
QR = None

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
        # Function that THREAD will do
        global QR
        while True:
            i = 0

            if self.name is 'QR':
                try:
                    QRTest = QRreader.ReadQR()
                except Exception:
                    with open("Syslog.txt", "a") as file:
                        file.writelines("\n[ERROR QR-read] : " + str(datetime.datetime.now()) + "]\n{"
                                        + " " + str(Exception) + " " + "[QR:VALUE] = " + str(QRTest)
                                        + "\n}END\n")
                        file.close()

                if QRTest is not None:
                    QRreader.camara()
                    if SOAPClient.Authentication(QRTest):
                        Voice.speak1("CodigoQRAceptado.mp3")
                        QR = QRTest
                        QRTest = None

                    else:
                        QRTest = None
                        Voice.speak1("CodigoQRdenegado.mp3")

            if self.name is 'Salida':
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
    if not GPIO.input(12):
        Motors.Open_Barrier_OUT()
        Motors.Open_Barrier_IN()
        Voice.speak1("BotonPanico.mp3")

        while not GPIO.input(12):
            Lights.Turn_ON_Full()
            time.sleep(2)
            Lights.Turn_OFF_Full()

        Motors.Close_Barrier_IN()
        Motors.Close_Barrier_OUT()


def EVALUACION():
    if not GPIO.input(SensorIR):

        print('[INFO] Cliente Recibido...\n [INFO] Evaluando Cliente...')

        if Contador.StatusLocalCapacity():

            # SENSOR DE TEMPERATURA

            tempe = TempC.ReadSensorTemp()
            if tempe > 50.0:
                print("[INFO] TEMPERATURA: " + str(tempe))
                Voice.speak1("ErrorTemperatura.mp3")
            else:

                if tempe < 38.0:
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

                    Contador.PriorityOFF()
                    Lights.Turn_OFF_Green()
                    Motors.Close_Barrier_IN()
                    print('[INFO] Acceso Prioritario Permitido...\n[INFO] Esperando Nuevo Cliente...')
                    return True

                elif (result == 'No Mask' or not TempSafe) and token:

                    Lights.Turn_ON_Red()
                    Voice.speak1('denegado.mp3')
                    print('[INFO] Acceso Prioritario Denegado...\n[INFO] Esperando Nuevo Cliente...')
                    Contador.Person(Temp=tempe, Mask=False, Entry=False)
                    Contador.PriorityOFF()
                    Lights.Turn_OFF_Red()
                    return True

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
            return True
    elif GPIO.input(SensorIR):
        return False

# Create Thread's
threadExit = myThread(1, "Salida")
threadQR = myThread(2, "QR")
threadExit.start()
threadQR.start()


def __main__():
    SOAPClient.InitializationSystem()
    print('[INFO] Sistema De Prioridad Activado...\n[INFO] Esperando Cliente...')
    Voice.speak1('bienvenido.mp3')

    global acces, tempe, QR
    while True:
        BotonPanico()
        if QR is not None:
            Contador.PriorityON(QR)
            status = True
            t1 = time.time()
            while status:
                t2 = time.time()
                if EVALUACION():
                    status = False
                    QR = None
                if (t2 - t1) > 10:
                    status = False
                    QR = None
                    print("[INFO] Tiempo De Espera Agotado")


if __name__ == '__main__':
    __main__()
    threadExit.join()
    threadQR.join()
