"""
                Autor: Edgard Jose Diaz Tipacamu
		e.diaz@nartsoft.com.mx
		27 de febrero de 2019

		Este codigo implementa el algoritmo de huffman para realizar
		la compresion de un un archivo de texto plano. para ello se
		genera un archivo el cual contiene las probabilidades de cada
		uno de los simbolos definidos en el diccionario de simbolos.
		
"""

"""
	Descripcion:

		* variable result_probabilidades: esta variable contiene el nombre del archivo que contiene las probabilidades
	de los simbolo que se encuentran en el texto a comprimir.

		* variable fichero: Esta variable contiene el nombre del archivo que se va a comprimir, en este caso el nombre
	del archivo se pasa comoa arumento desde la linea de comandos (ver. ejecucion).

		* 

	Ejecucion:
		python generardor_huffman_code.py -f NAME_FICHERO
"""
from decimal import Decimal
import sys
import os
import operator
result_probabilidades = "result.txt"
fichero = sys.argv[2]

def compresor_huffman():
	probabilidades = {}	
	tabla_codigos = {}
	
	line = ""
	archivo = open(result_probabilidades,'r');
	for i in  archivo:
		line = i.split("\t")

		if(line[0] == "space"):
			pass
		#	probabilidades[' '] = float(line[1].rstrip())
		elif(line[0]=="salto"):
			pass
		#	probabilidades["\n"] = float(line[1].rstrip())
		else:
			probabilidades[line[0]] = float(line[1].rstrip())
	#print probabilidades
	archivo.close()
	tabla_codigos = huffmanCode(probabilidades)
	#print tabla_codigos
	save_codes(tabla_codigos)
	
	with open(fichero,'r') as txt, open("comprimido.dat",'wb') as salida:
		txt = (txt.read().rstrip()).lower()
		
		encoded_text = TextEncode(tabla_codigos,txt)
		padded_encodded = PadEncode(encoded_text);
		CadenaBits = GeneraBitArray(padded_encodded)
		salida.write(bytes(CadenaBits))


# funcion que permite realizar el ordenamiento de las  probabilidades
def ordenar_probabilidades(dic):
	# la funcion sorted ordena el diccionario de probabilidades de menor a mayor 
	
	#ordenado = sorted(dic.items(), key = lambda (i, pi): pi);
	ordenado = sorted(dic.items(), key = operator.itemgetter(1), reverse=False)
	
	
	#retorna una tupla con las llaves del diccionario con respecto a las dos primeras probabilidad 
	#que en este caso son los dos simbolos menos probables.
	
	return ordenado[0][0], ordenado[1][0]

#	print probabilidades
def huffmanCode(dic):
	# realiza una copia del diccionario de probabilidades ya que mas adelante los elemntos que esta marcados
	# con las llaves que nos devuelve el metos ordenar_probabilidades seran removidas del diccionario original
#	assert(sum(dic.values()) == 1.0) # Ensure probabilities sum to 1

    # Base case of only two symbols, assign 0 or 1 arbitrarily
	if(len(dic) == 2):
		return dict(zip(dic.keys(), ['0', '1']))

    # Create a new distribution by merging lowest prob. pair
	p_copy = dic.copy()
	
	K1, K2 = ordenar_probabilidades(dic)

	p1, p2 = p_copy.pop(K1), p_copy.pop(K2)
	p_copy[K1 + K2] = p1 + p2
# Recurse and construct code on new distribution

	c = huffmanCode(p_copy)
	ca1a2 = c.pop(K1 + K2)
	c[K1], c[K2] = ca1a2 + '0', ca1a2 + '1'


	return c
#################################################################################
#Guardar el libro de codigos en fichero de texto plano
def save_codes(dic):
	file = open("codigos.txt","w")
	for i in dic:
#		print dic.get(0,i) +"\t"+ dic.get(i,i);
		if i == '\n':
			file.write("salto"+"\t"+ dic.get(i,i)+"\n");
		else:
			file.write(dic.get(0,i) +"\t"+ dic.get(i,i)+"\n");
	file.close();
###############################################################################

def TextEncode(codes, texto):

	encode_text = ""
	#print texto.split()
	for ch in texto.split():
		if ch in codes:
			#print(ch, codes[ch])
			encode_text += codes[ch]

	return encode_text

def PadEncode(encoded):
	padding = 8 - len(encoded) % 8

	for i in range(padding):
		encoded += "0"

	padded_info = "{0:08b}".format(padding)
	encoded = padded_info + encoded

	return encoded

def GeneraBitArray(cadena_binaria):
	if(len(cadena_binaria) % 8 != 0):
		exit(0)

	Cbits = bytearray()

	for i in range(0, len(cadena_binaria), 8):
		byte = cadena_binaria[i:i+8]
		Cbits.append(int(byte, 2))
	
	return Cbits


compresor_huffman()
print("\n\n")

"""
	Se realiza la obtencion del tamanio del archivo original y del archivo comprimido
	para mostrar los resultado en pantalla
"""
sizefile = os.path.getsize(sys.argv[2])
sizefile2 = os.path.getsize("comprimido.dat")
sizefile= sizefile/(1024*1024.0)
sizefile2 = sizefile2/(1024*1024.0)
porcentaje  = ((sizefile2/sizefile) * 100)


print ("Texto original: " +str(sys.argv[2])+ " Tamanio: "+ str(sizefile)+" MB")
print ("File comprimido: comprimido.dat Tamanio: " + str(sizefile2)+" MB")
print("Archivo "+sys.argv[2]+" comprimido en "+ str(round(porcentaje))+"%")
print("Archivo de texto comprimido :) !!\n\n")
