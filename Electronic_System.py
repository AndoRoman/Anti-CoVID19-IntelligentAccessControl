import Lights #MODULE TO LIGHTS
import Voice #MODULE TO VOICE
import ultrasonic_entrada #MODULE TO SENSORS
import ultrasonic_salida
#############
import threading
import time


####CLASS TO THREAD###
class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
       ##Function that THREAD will do
       while(1):
           if self.name == 'Salida':
               measure = ultrasonic_entrada.distance()
               if(measure < 60.00):
                   print('Sensor of: ' + self.name + " was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##
                   time.sleep(2)


           if self.name == 'Entrada':
               measure = ultrasonic_entrada.distance()
               if(measure < 60.00):
                   print('Sensor of: ' + self.name + " was activated. Measure: %.2f" % measure)
                   ##Stop thread for 2 second##
                   time.sleep(2)

##Create Thread's######
threadEntrace = myThread(1, "Entrada")
threadExit = myThread(2, "Salida")
threadEntrace.start()
threadExit.start()
#threadEXIT1 = myThread(2, 'Salida1', 1)
#threadEXIT2 = myThread(3, 'Salida2', 1)

def __main__():

    while(1):
        print('[INFO] Sistema Activado...\n[INFO] Esperando Cliente...')
        acces=input()

        if(acces=='si'):
            try:
                Voice.speak1('Acceso Permitido')
            except Exception as e:
                Voice.speak2('Acceso Permitido')
            Lights.Turn_ON_Green()
        elif(acces=='full'):
            try:
                Voice.speak1('Lo sentimos, el Local esta lleno. No puede pasar')
            except Exception as e:
                Voice.speak2('El local esta lleno')
            Lights.Turn_ON_Full()
        else:
            try:
                Voice.speak1('Acceso Denegado, No puede pasar')
            except Exception as e:
                Voice.speak2('Accesso Denegado  No puede pasar')
            Lights.Turn_ON_Red()


if __name__ == '__main__':
    __main__()
    threadEntrace.join()
    threadExit.join()
