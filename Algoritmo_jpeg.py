"""
    
    Centro de Investigacion y Estudios Avanzados del IPN
    
    Athor: Edgard Jose Diaz Tipacamu
    ediaz@tamps.cinvestav.mx

    Codificacion y compresion de datos.

    En este archivo fuente se realizo la implentacion del algoritmo de  comprension de imagenes
    JPEG.

    Para su ejecucion se hizo uso de las librerias 
        *   numpy 
        *   scipy 
        *   PIL
    Para instalar las librerias se usaron los comandos

        python -m pip install numpy scipy matplotlib
    
    El comando  anterior  realiza la instalacion  de numpy, matplotlib y scipy

    Para la instalacion de PIL
        pip install Pillow

"""



from scipy.fftpack import dct,idct
import scipy
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import os
import matplotlib.pyplot as plt

Z = [[16, 11, 10, 16, 24, 40, 51, 61],
     [12, 12, 14, 19, 26, 58, 60, 55],
     [14, 13, 16, 24, 40, 57, 69, 56],
     [14, 17, 22, 29, 51, 87, 80, 62],
     [18, 22, 37, 56, 68 ,109 ,103 ,77],
     [24, 35, 55, 64, 81 ,104 ,113 ,92],
     [49, 64, 78, 87, 103, 121, 120, 101],
     [72, 92, 95, 98, 112, 100, 103, 99]]
temporal = {}
frecuencia = {}

g = 0;

def dct2(a):
    new_matriz = np.zeros((8,8));
    b = np.zeros((8,8));
    #############################################################################################
    #
    #   Realizamos la resta de 128 a cada uno de los elementos
    #
    #############################################################################################
    for i in range(8):
        for j in range(8):
            b[i][j] = a[i][j] - 128;
    ##############################################################################################
    #
    #   Se Aplica la dct al bloque de 8x8
    #
    ##############################################################################################
    c = scipy.fftpack.dct( scipy.fftpack.dct( b, axis=0, norm='ortho' ), axis=1, norm='ortho' )


    ##############################################################################################
    #
    #   Se Normaliza el bloque de 8x8
    #
    ##############################################################################################

    for i in range(8):
        for j in range(8):
            new_matriz[i][j] = np.fix(c[i][j]/Z[i][j]) # fix realiza redondeo a piso
    
    return new_matriz


def zigzag(matrix):
    global g
    con = 0
    matrix = np.array(matrix)
    rows=8
    columns=8
    aux = np.zeros((1,64))
    x = np.zeros((1,64))
    y = np.zeros((1,64))

    """  Implemtacion del ordenamiento de bloques en zigzag
         recuperada de la url: https://www.geeksforgeeks.org/print-matrix-zag-zag-fashion/"""
    solution=[[] for i in range(rows+columns-1)]
    
    for i in range(rows): 
        for j in range(columns): 
            sum=i+j
            
            if(sum%2 ==0):
                solution[sum].insert(0,matrix[i][j]) 
            
            else:
                solution[sum].append(matrix[i][j])
              
    solucion = solution.reverse()
#    f = open("zig.txt", "a")
    for i in solution:
        for j in i:
            if j == -0.0:
                j = abs(j)
                aux[0,con] = j
            else:
                aux[0,con] = j #Se guarda en vector el resultado del ordenamiento zigzag
            con = con + 1;
    
    indice = 0;

    for i in range(0,64):
        if(aux[0,i]!= 0):
            indice = i
            break

    for i in range(indice,64):
        
        temporal[g] = aux[0,i];

        if aux[0,i] in frecuencia:
            pass
        
        else:
            frecuencia[aux[0,i]] = aux[0,i]
        g = g+1

"""Esta funcion realiza la escritura del archivo de probabilidades"""
def save_probabilidades(dic,keys):
    pos = 0;
    file = open("result.txt","w")
    for i in probabilidades:
        file.write(str(keys[pos]) +"\t"+ str(dic.get(i,i))+"\n");
        pos+= 1



"""Se realiza la carga de la imagen """
matrix = Image.open("lena.jpg")
matrix.show()
"""Se transforma la imagen a escala de grises """
matrix = matrix.convert('L')
matrix.save("gray.jpg")
matrix.show()

"""Se obtiene el alto y ancho de la imagen"""
alto, ancho = matrix.size

"""Parseamos la matriz que nos da la imagen a tipo flotante"""
a = np.asarray(matrix,dtype=np.float32)

"""Guardamos la imagenobtenida de la resta de los 128"""
alternativo  = a;
alternativo = alternativo - 128;

Image.fromarray(alternativo.astype(np.uint8)).save("restada.jpg")
I = Image.open("restada.jpg");
I.show()
"""Inicializamos una matriz de ceros de 256 x 256 la cual nos servira para guardar resultado del procesamiento"""
im2 = np.zeros((256,256))
##########################################################################################
#
#                   """Inicia Implementacion del algoritmo JPEG"""
#
##########################################################################################
for i in range(0,alto,8):
    for j in range(0,ancho,8):
        im2[i:(i+8),j:(j+8)] = dct2(a[i:(i+8),j:(j+8)])


"""Guardamos la imagen obtenida al realizar la DTC 2D"""

Image.fromarray(im2.astype(np.uint8)).save("dct.jpg")
I = Image.open("dct.jpg");
I.show()

for i in range(0,alto,8):
        for j in range(0,ancho,8):
            zigzag(im2[i:(i+8),j:(j+8)])

"""Se Realiza el ordenamiento en zigzag  de los bloques de 8x8"""

f = open("dct.txt","w")
for i in range(0,alto):
    for j in range(0,ancho):
        if im2[i,j] == -0.0:
            f.write(str(abs(im2[i,j]))+" ")
        else:
            f.write(str(im2[i,j])+" ")
    f.write("\n")


keys = frecuencia.keys()
elementos = temporal.values()

tam = len(keys)

probabilidades = {}

for i in keys:
    telemento = float(elementos.count(i));
    #print i;
    probabilidades[i] = telemento/float(len(elementos));

    #keys[i];
save_probabilidades(probabilidades,keys)

print("Se a realizado exitosamente el procesamiento de la imagen. \n Se ha generado un archivo de probabilidades.\n Se ha generado el archivo de texto que contiene la matriz resultante del procesamiento de JPEG")

#print len(probabilidades)
#zigzag(matrix)