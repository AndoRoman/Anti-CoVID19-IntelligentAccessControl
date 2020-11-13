import Lights #MODULE TO LIGHTS
import Voice #MODULE TO VOICE

print('Escriba "si" si el individuo puede pasar o "no" sino puede. \nY si el local está lleno escriba: "full" ')
acces=input()

if(acces=='si'):
    try:
        Voice.speak1('Acceso Permitido')
    except Exception as e:
        Voice.speak2('Acceso Permitido')
    Lights.Turn_ON_Green()
elif(acces=='full'):
    try:
        Voice.speak1('Lo sentimos, el Local esta lleno. No puede pasar')
    except Exception as e:
        Voice.speak2('El local esta lleno')
    Lights.Turn_ON_Full()
else:
    try:
        Voice.speak1('Acceso Denegado, No puede pasar')
    except Exception as e:
        Voice.speak2('Accesso Denegado  No puede pasar')
    Lights.Turn_ON_Red()
