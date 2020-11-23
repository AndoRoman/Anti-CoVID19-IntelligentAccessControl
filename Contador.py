import linecache
import SOAPClient

# READ DATA
MaxCapacidad = linecache.getline("SucursalInfo.txt", 1).strip().split("=")[1]
Conteo = linecache.getline("SucursalInfo.txt", 2).strip().split("=")[1]

# PRIORITY
Priority = False
QR = None
print("[INFO] Contador Inicializado...")


def PriorityON(qrImage):
    global Priority, QR
    Priority = True
    QR = qrImage


def PriorityOFF():
    global Priority, QR
    Priority = False
    QR = None


def Person(Temp, Mask):
    global Conteo, Priority
    if Priority:
        Conteo = SOAPClient.UpdateStatus(Temp=Temp, Mask=Mask, QR=QR)[1]
    else:
        Conteo = SOAPClient.UpdateStatus(Temp=Temp, Mask=Mask, QR=None)[1]


def DeletePerson():
    global Conteo
    Conteo -= 1
    SOAPClient.ExitPerson()


def ShowPerson():
    global Conteo
    return Conteo


def CanExitPerson():
    global Conteo
    if Conteo > 0:
        return True
    else:
        return False


def StatusLocalCapacity():
    global Conteo, MaxCapacidad
    if Conteo < MaxCapacidad:
        return True
    elif Conteo == MaxCapacidad:
        return False
