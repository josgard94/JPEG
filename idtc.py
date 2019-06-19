"""  
    Athor: Edgard Jose Diaz Tipacamu
    e.diaz@nartsoft.com.mx
    Codificacion y compresion de datos.

    En este codigo fuente se realiza el proceso inverso del algoritmo JPEG,
    con el cual se recupera la imagen comprimida con JPEG.

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

from math import cos,sin,pi
from scipy.fftpack import dct,idct
import scipy
import numpy as np
import random
from PIL import Image, ImageDraw,ImageFont
import os

Z = [[16, 11, 10, 16, 24, 40, 51, 61],
     [12, 12, 14, 19, 26, 58, 60, 55],
     [14, 13, 16, 24, 40, 57, 69, 56],
     [14, 17, 22, 29, 51, 87, 80, 62],
     [18, 22, 37, 56, 68 ,109 ,103 ,77],
     [24, 35, 55, 64, 81 ,104 ,113 ,92],
     [49, 64, 78, 87, 103, 121, 120, 101],
     [72, 92, 95, 98, 112, 100, 103, 99]]


""" Esta funcion realiza los pasos para recuperar la imagen comprimda por JPEG"""
def idct2(matrix):
	b = np.zeros((8,8));
	new_matrix = np.zeros((8,8));

	"""Se multiplican los bloques de 8x8 con la matriz de normalizacion"""
	for i in range(8):
		for j in range(8):
			b[i][j] = matrix[i][j] * Z[i][j];

	"""Se realiza el calculo de la IDCT"""
	c = scipy.fftpack.idct(scipy.fftpack.idct(b,axis=0, norm='ortho'),axis=1, norm='ortho')

	"""Se le suma 128 aca elemento del bloque de 8x8"""
	for i in range(8):
		for j in range(8):
			new_matrix[i][j] = c[i][j] + 128;
	return new_matrix

"""Cargamos la matriz obtenida del proceso de JPEG"""
matrix = np.loadtxt("matriz.txt",dtype=float)

matrix = np.array(matrix)
imagen = np.zeros((256,256))

for i in range(0,256,8):
	for j in range(0,256,8):
		imagen[i:(i+8), j:(j+8)] = idct2(matrix[i:(i+8), j:(j+8)])

"""Se muestra la imagen recueperada"""
Image.fromarray(imagen.astype(np.uint8)).save("comprimida.jpg")
I = Image.open("comprimida.jpg");
I.show()
