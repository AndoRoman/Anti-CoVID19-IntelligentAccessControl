import SOAPClient

# READ DATA
MaxCapacidad = 0
Conteo = 0
# PRIORITY
Priority = False
QR = None


def InitCount(Max, Count):
    global MaxCapacidad, Conteo
    MaxCapacidad = Max
    Conteo = Count
    print("[INFO] Contador Inicializado...")


def PriorityON(qrImage):
    global Priority, QR
    Priority = True
    QR = qrImage
    print("PRIORIDAD ACTIVADA, QR = " + QR)


def PriorityOFF():
    global Priority, QR
    Priority = False
    QR = None


def Person(Temp, Mask, Entry):
    global Conteo, Priority
    if Priority:
        Conteo = SOAPClient.UpdateStatus(Type=True, Temp=Temp, Mask=Mask, QR=QR, Entry=Entry)
    else:
        Conteo = SOAPClient.UpdateStatus(Type=False, Temp=Temp, Mask=Mask, QR=None, Entry=Entry)


def DeletePerson():
    global Conteo
    Conteo -= 1
    SOAPClient.ExitPerson()
    print("ALGUIEN SALIÓ CONTEO = " + str(Conteo))


def ShowPerson():
    global Conteo
    return Conteo


def CanExitPerson():
    global Conteo
    if int(Conteo) > 0:
        return True
        print("CANExitPerson = TRUE")
    else:
        return False


def StatusLocalCapacity():
    global Conteo, MaxCapacidad
    print("Conteo = " + str(Conteo) + " MaxCapacidad = " + str(MaxCapacidad))
    if int(Conteo) < int(MaxCapacidad):
        return True
    elif int(Conteo) == int(MaxCapacidad) or int(Conteo) < 0:
        return False
