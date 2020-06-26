import Lights #MODULE TO LIGHTS
import Voice #MODULE TO VOICE
import ultrasonic #MODULE TO SENSORS
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
           measure = ultrasonic.distance()
           if(measure < 60.00):
               print('Sensor of: ' + self.name + " was activated. Measure: %.2f" % measure)
               ##Stop thread for 2 second##
               time.sleep(2)
               
##Create Thread's######
threadEntrace = myThread(1, "Entrada")
threadEntrace.start()
#threadEXIT1 = myThread(2, 'Salida1', 1)
#threadEXIT2 = myThread(3, 'Salida2', 1)

def __main__():
    ##Start Thread##
    
    #threadEXIT1.start()
    #threadEXIT2.start()
    ###Main THREAD###
    while(1):
        print('Escriba "si" si el individuo puede pasar o "no" sino puede. \nY si el local está lleno escriba: "full" ')
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
            print("RED")
    

if __name__ == '__main__':
    __main__()
    threadEntrace.join()
    
