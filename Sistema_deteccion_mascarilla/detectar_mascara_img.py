import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# modelo de deteccion de rostro obtenido de: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# cargando directorio del modelo
modelo = 'P5__modeloClasificador.h5'
pesos = 'P5_pesos.h5' # 'pesos.h5'

# convirtiendo archivo serializado al modelo.
modeloCargado = load_model(modelo)
modeloCargado.load_weights(pesos)

def detectarMascara(im):
    predicionMascara = 0.00 #con mascara
    rostroDectado = 0
    #realizando modificaciones a imagen para ser procesada
    im=cv2.flip(im,1,1) #Flip to act as a mirror
    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))
    
    # detect MultiScale / faces 
    faces = classifier.detectMultiScale(mini)

    a = len(faces) #cantidad de rostro
    if a < 0 :
        print('No se ha detectado ningun rostro')
        print('')
        rostroDectado = 0
    else:
        rostroDectado = a
        #print('Cantidad de restro detectado: ')
        #print(a)
        #print('')
        for f in faces:
            (x, y, w, h) = faces[0]
            #Scale the shapesize backup
            #Save just the rectangle faces in SubRecFaces
            face_img = im[y:y+h, x:x+w]
            resized=cv2.resize(face_img,(150,150))
            normalized=resized/255.0
            reshaped=np.reshape(normalized,(1,150,150,3))
            reshaped = np.vstack([reshaped])
            result=modeloCargado.predict(reshaped)
            valor = result[0]
            #print('')
            #print('Sin mascara =')
            #print(valor[0]*100)
            #print('CON mascara =')
            #print(valor[1]*100)
            #print('')
            predicionMascara = valor[1]*100
    return (rostroDectado, predicionMascara) 

#simulacion
#realizando prueba con imagenes estaticas! 
estado = True
while estado:
    print('Digite la dirrecion de la foto:')
    imagepath = input() 
    im=cv2.imread(str(imagepath))
    (CantRostro, predicionMascara) = detectarMascara(im)
    print(CantRostro)
    print(predicionMascara)

    
        