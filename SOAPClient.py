# import zeep
import linecache
import datetime
import Controlador

# CLIENT SOAP
# settings = zeep.Settings(strict=False, xml_huge_tree=True)
# wsdl = 'URL_SERVER_SOAP_DOC_soap'

# cliente = Client(wsdl)
# Factory more information on Doc : https://docs.python-zeep.org/en/master/datastructures.html
# factory = cliente.type_factory('http://soap.clienteHTML5/')

# information Pre-configurate
ModuloID = linecache.getline("configuration.txt", 1).strip().split("=")[1]
# ModuloEstatus indica si es normal (0) o Prioritario (1)
ModuloEstatus = linecache.getline("configuration.txt", 2).strip().split("=")[1]
IDSucursal = linecache.getline("configuration.txt", 3).strip().split("=")[1]
print("[INFO] SOAPClient Inicializado...")


# Initialization
def InitializationSystem():
    # response = MaxCapacidad de la sucursal
    response = cliente.service.inicializar(IDSucursal)

    with open("Syslog.txt", "a") as file:
        file.writelines("\n[Initialization : " + str(datetime.datetime.now()) +
                        "]\n{" + str(response) + "\n}END\n")
        file.close()

    with open("SucursalInfo.txt", "w+") as data:
        data.writelines("MaxCapacidad=" + str(response) + "\nContador=0")
        data.close()


def NewTest(Temp, Mask, QR):
    test = factory.DtoTesting(mascarilla=Mask, temperatura=Temp, fechaRegistro=datetime.datetime.now(),
                              idModulo=ModuloID, tipoModulo=ModuloEstatus, cedulaPersona=QR)
    return test


# Enviar Nuevo Test
def UpdateStatus(Temp, Mask, QR):
    count = cliente.service.agregarTest(NewTest(Temp=Temp, Mask=Mask, QR=QR))  # Retorna nuevo valor de conteo

    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ PUSH TO CLOUD : " + str(test.fechaRegistro) + "]\n{"
                        + "ModuloID = " + str(ModuloID)
                        + "\nPersonas dentro del Local = " + str(count[1])
                        + "\n}END\n")
        file.close()
    return count


def ExitPerson():
    return cliente.service.salidadDePersona(IDSucursal)


# Authenticar QR
def Authentication(QR):
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ Authenticate QR : " + str(datetime.datetime.now()) + "]\n{}END\n")
        file.close()
    return cliente.service.consultarPrioridad(QR, IDSucursal)  # True or False


def __main__():
    print("Archivo de Configuración:\n ModuloID = " + str(ModuloID) + "\n ModuloEstatus = " + str(ModuloEstatus) +
          "\n IDSucursal = " + str(IDSucursal))


if __name__ == '__main__':
    __main__()
