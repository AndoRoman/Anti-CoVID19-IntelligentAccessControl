from gtts import gTTS #LIBRARY GOOGLE pip3 install gTTS
from playsound import playsound # LIBRARY GOOGLE pip3 install playsound

def crearVoice(text, idioma):
    tts = gTTS(text,  lang=idioma)
    with open("ArchivoVoz.mp3", "wb") as archivo:
         tts.write_to_fp(archivo)
def speak1(text):
    idioma = 'es-es'
    crearVoice(text, idioma)
    playsound('ArchivoVoz.mp3')#Permite reproducir el audio.


### TEST ####
def __main__():
    speak1('Acceso Permitido pase por favor')

if __name__ == '__main__':
    __main__()
