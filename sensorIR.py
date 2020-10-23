import RPi.GPIO as IO
import time
import threading
IO.setwarnings(False)
IO.setmode(IO.BCM)

Led = 18
Rec1 = 23
Rec2 = 24
IO.setup(Led,IO.OUT) #GPIO 3 -> IR tranmiter data
IO.setup(Rec1, IO.IN, pull_up_down=IO.PUD_UP) #INTERRUPTION MODE TO INPUT sensor
IO.setup(Rec2,IO.IN, pull_up_down=IO.PUD_UP)
####CLASS TO THREAD###
class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
       ##Function that THREAD will do
       while(1):
           if IO.input(Rec1) == False:
               print('[INFO] Receptor1 Activated!')
               time.sleep(2)
               
               
   
##Create Thread's######
threadIR1 = myThread(1, "Receptor1")
#threadIR2 = myThread(2, "Receptor2")
threadIR1.start()
#threadIR2.start()

def __main__():
    print("[INFO] Starting Program...")
    IO.output(Led, IO.HIGH)
    while True:
        if IO.input(Rec2) == False:
            print('[INFO] Receptor2 Activated!')
            time.sleep(2)
        
        
if __name__ == '__main__':
    __main__()
    threadIR1.join()
    #threadIR2.join()

