from gtts import gTTS #LIBRARY GOOGLE pip3 install gTTS
from playsound import playsound
#import pyttsx3 #LIBRARY TO VOICE pip3 install pyttsx3
import os

def crearVoice(text, idioma, nombreArchivo):
    tts = gTTS(text,  lang=idioma)
    with open(nombreArchivo, "wb") as archivo:
         tts.write_to_fp(archivo)


def speak1(archivo):
    #playsound(archivo) #PC
    os.system('omxplayer ' + archivo) #PI

### TEST ####
def __main__():
    while(1):
        print("1 para crear archivo - 2 para reproducir uno - q para salir")
        option = input()
        if(option == '1'):
            print("Nombre de archivo: ")
            archivo = input()
            print("Mensaje: ")
            text = input()
            crearVoice(text, 'es-es', archivo)
        if(option == '2'):
            print("Archivo: ")
            nombre = input()
            speak1(nombre)
        if(option == 'q'):
            break
    

if __name__ == '__main__':
    __main__()
