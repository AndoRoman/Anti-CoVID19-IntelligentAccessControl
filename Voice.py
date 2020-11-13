from gtts import gTTS #LIBRARY GOOGLE pip3 install gTTS
from playsound import playsound # LIBRARY GOOGLE pip3 install playsound
import pyttsx3 #LIBRARY TO VOICE pip3 install pyttsx3

def crearVoice(text, idioma):
    tts = gTTS(text,  lang=idioma)
    with open("ArchivoVoz.mp3", "wb") as archivo:
         tts.write_to_fp(archivo)
def speak1(text):
    idioma = 'es-es'
    crearVoice(text, idioma)
    playsound('ArchivoVoz.mp3')#Permite reproducir el audio.

####### IF WE DON'T HAVE CONNECTION #################
engineio = pyttsx3.init() # object creation
voices = engineio.getProperty('voices') #getting details of current voice
engineio.setProperty('rate', 140)    # Aquí puedes seleccionar la velocidad de la voz
engineio.setProperty('voice',voices[4].id) #changing index, changes voices. o for male

def speak2(text): #funcion que convierte texto a voz
    engineio.say(text)
    engineio.runAndWait()

### TEST ####
def __main__():
    speak1('Acceso Permitido pase por favor')

if __name__ == '__main__':
    __main__()
