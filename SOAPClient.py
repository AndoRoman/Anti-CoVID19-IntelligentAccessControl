import linecache
import datetime

# CLIENT SOAP
from zeep import *

import Contador

settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://aciacs.azrael.studio/ws?wsdl'
#wsdl = 'http://localhost:7000/ws?wsdl'

cliente = Client(wsdl)
# Factory more information on Doc : https://docs.python-zeep.org/en/master/datastructures.html
factory = cliente.type_factory('http://Soap.ACIACS/')

# information Pre-configurate
ModuloID = linecache.getline("Configuration", 1).strip().split("=")[1]
# ModuloEstatus indica si es normal (0) o Prioritario (1)
ModuloEstatus = linecache.getline("Configuration", 2).strip().split("=")[1]
IDSucursal = linecache.getline("Configuration", 3).strip().split("=")[1]


# Initialization
def InitializationSystem():
    # response = MaxCapacidad de la sucursal
    response = cliente.service.capacidadSucursal(IDSucursal)
    if int(response[0]) > 0:
        with open("Syslog.txt", "a") as file:
            file.writelines("\n[Initialization : " + str(datetime.datetime.now()) +
                            "]\n{MaxCapacidad de la Sucursal = " + str(response[0]) + "\n}END\n")
            file.close()

        Contador.InitCount(Max=response[0], Count=response[1])


def NewTest(typeID, Temp, Mask, QR, Entry):
    if typeID == 2:
        #PRIORITY
        test = factory.dtoTesting(mascarilla=Mask, temperatura=Temp, fechaResgistro=datetime.datetime.now(),
                                  idModulo=typeID, tipoModulo=False, cedulaPersona=QR, estatus=Entry)
    else:
        test = factory.dtoTesting(mascarilla=Mask, temperatura=Temp, fechaResgistro=datetime.datetime.now(),
                                  idModulo=typeID, tipoModulo=True, cedulaPersona=QR, estatus=Entry)

    return test


# Enviar Nuevo Test
def UpdateStatus(Type, Temp, Mask, QR, Entry):
    if Type:
        # Priority
        count = cliente.service.agregarTest(NewTest(typeID=2, Temp=Temp, Mask=Mask, QR=QR, Entry=Entry))
    else:
        # Normal
        count = cliente.service.agregarTest(
            NewTest(typeID=1, Temp=Temp, Mask=Mask, QR=QR, Entry=Entry))  # Retorna nuevo valor de conteo
    # with open("Syslog.txt", "a") as file:
    #     file.writelines("\n[ PUSH TO CLOUD : " + str(datetime.datetime.now()) + "]\n{"
    #                     + "ModuloID = " + str(ModuloID)
    #                     + "\nTEST = " + str(Temp) + ", " + str(Mask) + ", " + str(QR)
    #                     + "\nPersonas dentro del Local = " + str(count[1])
    #                     + "\n}END\n")
    #     file.close()
    return count[1]


def ExitPerson():
    return cliente.service.salidadDePersona(IDSucursal)


# Authenticar QR
def Authentication(QR):
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ Authenticate QR : " + str(datetime.datetime.now()) + " QR: " + str(QR) + "]\n{}END\n")
        file.close()
    return cliente.service.consultarPrioridad(QR, IDSucursal)


def __main__():
    InitializationSystem()
    print("Conectado")
    print('autenticar: ' + str(Authentication("402-1409395-3")))
    print('Agregando persona: ' + str(UpdateStatus(True, 37.5, True, '402-1409395-3', True)))
    print('ModuloID: ' + ModuloID + ' sucursal: ' + IDSucursal)


if __name__ == '__main__':
    __main__()
