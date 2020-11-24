# import Voice
import linecache
import datetime

# CLIENT SOAP
from zeep import *

settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://aciacs.azrael.studio/ws?wsdl'
# wsdl = 'http://localhost:7000/ws?wsdl'

cliente = Client(wsdl)
# Factory more information on Doc : https://docs.python-zeep.org/en/master/datastructures.html
factory = cliente.type_factory('http://Soap.ACIACS/')

# information Pre-configurate
ModuloID = linecache.getline("configuration.txt", 1).strip().split("=")[0]
# ModuloEstatus indica si es normal (0) o Prioritario (1)
ModuloEstatus = linecache.getline("configuration.txt", 2).strip().split("=")[0]
IDSucursal = linecache.getline("configuration.txt", 3).strip().split("=")[0]



# Initialization
def InitializationSystem():
    # response = MaxCapacidad de la sucursal
    response = cliente.service.capacidadSucursal(str(1))

    if (int(response[0]) > 0):
        with open("Syslog.txt", "a") as file:
            file.writelines("\n[Initialization : " + str(datetime.datetime.now()) +
                            "]\n{MaxCapacidad de la Sucursal = " + str(response[0]) + "\n}END\n")
            file.close()

        with open("SucursalInfo.txt", "w+") as data:
            data.writelines("MaxCapacidad=" + str(response[0]) + "\nContador=" + str(response[1]))
            data.close()



def NewTest(typeID, Temp, Mask, QR, Entry):
    if type == 2:
        test = factory.dtoTesting(mascarilla=Mask, temperatura=Temp, fechaResgistro=datetime.datetime.now(),
                                  idModulo=typeID, tipoModulo=False, cedulaPersona=QR, estatus=Entry)
    else:
        test = factory.dtoTesting(mascarilla=Mask, temperatura=Temp, fechaResgistro=datetime.datetime.now(),
                                  idModulo=typeID, tipoModulo=True, cedulaPersona=QR, estatus=Entry)

    return test


# Enviar Nuevo Test
def UpdateStatus(Temp, Mask, QR, Entry):
    if QR is not None:
        # Priority
        count = cliente.service.agregarTest(NewTest(2, Temp=Temp, Mask=Mask, QR=QR, Entry=Entry))
    else:
        # Normal
        count = cliente.service.agregarTest(
            NewTest(1, Temp=Temp, Mask=Mask, QR=QR, Entry=Entry))  # Retorna nuevo valor de conteo

    # with open("Syslog.txt", "a") as file:
    #     file.writelines("\n[ PUSH TO CLOUD : " + str(datetime.datetime.now()) + "]\n{"
    #                     + "ModuloID = " + str(ModuloID)
    #                     + "\nTEST = " + str(Temp) + ", " + str(Mask) + ", " + str(QR)
    #                     + "\nPersonas dentro del Local = " + str(count[1])
    #                     + "\n}END\n")
    #     file.close()
    return count[1]


def ExitPerson():
    return cliente.service.salidadDePersona(str(1))


# Authenticar QR
def Authentication(QR):
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ Authenticate QR : " + str(datetime.datetime.now()) + "]\n{}END\n")
        file.close()
    return cliente.service.consultarPrioridad(QR, str(1))  # True or False


def __main__():
    InitializationSystem()
    print("Conectado")
    print('Agregando persona: ' + str(UpdateStatus(37.5, True, None, True)))
    print('autenticar: ' + str(Authentication("1323143243")))
    print('Salida: ' + str(ExitPerson()))


if __name__ == '__main__':
    __main__()
