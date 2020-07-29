import Lights #MODULE TO LIGHTS
import Voice #MODULE TO VOICE
import ultrasonic_entrada #MODULE TO SENSORS
import ultrasonic_salida
import Dect_Image#MODULE TO AI MASK
import RPi.GPIO as GPIO
#############
import threading
import time


#####VARIABLES###########
Contador = 0;
MaxCapacidad = 60;#Max people into building


###GPIO###
SensorIR = 12
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(SensorIR, GPIO.IN, initial=GPIO.HIGH) #sensor IR



####CLASS TO THREAD###
class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
       ##Function that THREAD will do
       global Contador
       while(1):
           if self.name == 'Salida':
               measure = ultrasonic_salida.distance()
               if(measure < 60.00):
                   print('Sensor of: ' + self.name + " was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##
                   Contador -= 1
                   time.sleep(2)


           if self.name == 'Entrada':
               measure = ultrasonic_entrada.distance()
               if(measure < 60.00):
                   print('Sensor of: ' + self.name + " was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##
                   Contador += 1
                   time.sleep(2)

##Create Thread's######
threadEntrace = myThread(1, "Entrada")
threadExit = myThread(2, "Salida")
threadEntrace.start()
threadExit.start()
#threadEXIT1 = myThread(2, 'Salida1', 1)
#threadEXIT2 = myThread(3, 'Salida2', 1)

def __main__():
    print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
    while(1):

        acces = False

        if(!GPIO.input(SensorIR)):
            acces = True
            print('[INFO] Cliente Recibido...\n [INFO] Evaluando Cliente...')

            if(Contador<MaxCapacidad and acces):
                try:
                    result = Dect_Image.Reconocimiento()
                    token = True
                except Exception as e:
                    print('[INFO] ¡Error de Reconocimiento Facial!')
                    token = False


                print('[INFO] Evaluacion Concluida...\n [INFO] Enviando Resultandos...')

                if(result=='Mask' and token):
                    try:
                        Voice.speak1('Acceso Permitido')
                    except Exception as e:
                        Voice.speak2('Acceso Permitido')
                    Lights.Turn_ON_Green()
                    print('[INFO] Acceso Permitido...\n[INFO] Esperando Nuevo Cliente...')

                elif(result=='No Mask' and token):
                    try:
                        Voice.speak1('Acceso Denegado, No puede pasar')
                    except Exception as e:
                        Voice.speak2('Accesso Denegado  No puede pasar')
                    Lights.Turn_ON_Red()
                    print('[INFO] Acceso Denegado...\n[INFO] Esperando Nuevo Cliente...')

                if(!token):
                    print('[INFO] Intentelo de Nuevo...')
                    try:
                        Voice.speak1('Intentelo de Nuevo')
                    except Exception as e:
                        print('[INFO] ¡ERROR DE CONEXIÓN!')

            elif(Contador==MaxCapacidad):
                try:
                    Voice.speak1('Lo sentimos, el Local esta lleno. No puede pasar')
                except Exception as e:
                    Voice.speak2('El local esta lleno')
                    Lights.Turn_ON_Full()
                    print('[INFO] Local Lleno...\n[INFO] No se permiten Nuevos Clientes...')

if __name__ == '__main__':
    __main__()
    threadEntrace.join()
    threadExit.join()
