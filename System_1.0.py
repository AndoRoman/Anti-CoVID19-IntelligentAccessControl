import Lights #MODULE TO LIGHTS
from Alertas import Voice #MODULE TO VOICE
import ultrasonic_entrada #MODULE TO SENSORS
import ultrasonic_salida
import Dect_Image#MODULE TO AI MASK
import RPi.GPIO as GPIO
#############
import threading
import time


#####VARIABLES###########
Contador = 0;
MaxCapacidad = 2;#Max people into building


###GPIO###
SensorIR = 4
SensorSalida = 24
SensorEntrada = 23
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(SensorIR, GPIO.IN) #sensor IR



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
           
           if(self.name == 'Salida'):
               if (not GPIO.input(SensorSalida)):
                   if(Contador>0):
                       #print("Una persona ha SALIDO...")
                       Contador -= 1
                       print("SALIDA.. Cantidad de personas: " + str(Contador))
                       Lights.Turn_OFF_Full()
                       time.sleep(1)

                   #print(self.name + ": was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##



           if self.name == 'Entrada':
               #measure1 = ultrasonic_entrada.distance()
               if( not GPIO.input(SensorEntrada)):
                   if(Contador<MaxCapacidad):
                       Contador += 1
                       print("ENTRADA...Cantidad de personas: " + str(Contador))
                       time.sleep(1)
                       if(Contador==MaxCapacidad):
                           Lights.Turn_ON_Full()
                           Voice.speak1('MaxCapacidad.mp3')
               
                   
                   #print(self.name + ": was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##
                   

##Create Thread's######
threadEntrace = myThread(1, "Entrada")
threadExit = myThread(2, "Salida")
threadEntrace.start() #Inicialization Thread
threadExit.start() 
#threadEXIT1 = myThread(2, 'Salida1', 1)
#threadEXIT2 = myThread(3, 'Salida2', 1)

def __main__():
    #Voice.crearVoice()
    print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
    Voice.speak1('bienvenido.mp3')
    while(1):

        acces = False

        if(not GPIO.input(SensorIR)):
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
                    Lights.Turn_ON_Green()
                    Voice.speak1('aceptado.mp3')
                    print('[INFO] Acceso Permitido...\n[INFO] Esperando Nuevo Cliente...')
                    Lights.Turn_OFF_Green()

                elif(result=='No Mask' and token):
                    Lights.Turn_ON_Red()
                    Voice.speak1('denegado.mp3')
                    print('[INFO] Acceso Denegado...\n[INFO] Esperando Nuevo Cliente...')
                    Lights.Turn_OFF_Red()

                if(not token):
                    print('[INFO] Intentelo de Nuevo...')
                    try:
                        Voice.speak1('error.mp3')
                    except Exception as e:
                        print('[INFO] ¡ERROR DE CONEXIÓN!')

            elif(Contador==MaxCapacidad):
                ## Pero el contador no puede llegar al max
                Lights.Turn_ON_Full()
                Voice.speak1('localFull.mp3')
                print('[INFO] Local Lleno...\n[INFO] No se permiten Nuevos Clientes...')
                #Lights.Turn_OFF_Full()
            #elif(Contador<MaxCapacidad):
                #Lights.Turn_OFF_Full()
                

if __name__ == '__main__':
    __main__()
    threadEntrace.join()
    threadExit.join()
