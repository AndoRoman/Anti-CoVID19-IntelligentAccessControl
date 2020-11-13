# import zeep
import linecache
import datetime

# CLIENT SOAP
# settings = zeep.Settings(strict=False, xml_huge_tree=True)
# wsdl = 'URL_SERVER_SOAP_DOC_soap'

# cliente = Client(wsdl)
# Factory more information on Doc : https://docs.python-zeep.org/en/master/datastructures.html
# factory = cliente.type_factory('http://soap.clienteHTML5/')

# information Pre-configurate
ModuloID = linecache.getline("configuration.txt", 1).strip().split("=")[1]
ModuloEstatus = linecache.getline("configuration.txt", 2).strip().split("=")[1]
IDSucursal = linecache.getline("configuration.txt", 3).strip().split("=")[1]


# Initialization
def InitializationSystem():
    response = cliente.service.inicializar(ModuloID, ModuloEstatus, IDSucursal)
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[Initialization : " + str(datetime.datetime.now()) +
                        "]\n{" + str(response) + "\n}END\n")
        file.close()


def UpdateStatus():
    cliente.service.Status(ModuloID, Contador, GoodTest, BadTest)
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ PUSH TO CLOUD : " + str(datetime.datetime.now()) + "]\n{"
                        + "ModuloID = " + str(ModuloID)
                        + "\nPersonas dentro del Local = " + str(Contador)
                        + "\nPersonas con Acceso PERMITIDO = " + str(GoodTest)
                        + "\nPersonas con Acceso DENEGADO = " + str(BadTest)
                        + "\n}END\n")
        file.close()


# Authenticar QR
def Authentication(QR):
    with open("Syslog.txt", "a") as file:
        file.writelines("\n[ Authenticate QR : " + str(datetime.datetime.now()) + "]\n{}END\n")
        file.close()
    return cliente.service.autenticarQR(QR)  # True or False


def __main__():
    print("Archivo de Configuración:\n ModuloID = " + str(ModuloID) + "\n ModuloEstatus = " + str(ModuloEstatus) +
          "\n IDSucursal = " + str(IDSucursal))


if __name__ == '__main__':
    __main__()
