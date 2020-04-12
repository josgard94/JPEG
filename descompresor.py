"""
	Autor: Edgard Jose Diaz Tipacamu
	e.diaz@nartsoft.com.mx
	27 de febrero de 2019
	
	Este codigo fuente realiza la descompresion, de un archivo comprimido usando el
	programa generar_huffman_code.py

	Descripcion:
		El programa usa como entrada por argumento desde consola el nombre del archivo
		generado con el programa compresor (generar_huffman_code.py).
	
	Ejecucion:
		python descompresor.py -f FILE_NAME
"""
import sys

#Leemos como argumento desde consola el  nombre del archivo que queremos  descomprimir
fichero = sys.argv[2]

#Metodo que ejecuta la logica del programa realizando llamadas a otros metodos que 
#realizan tareas especificas.
def descomprimir():
#Cargamos el archivo que vamos a descomprimir se usa 'rb' para indicar que el archivo
#al que se hace refencia se leera en modo binario
	file = open(fichero,'rb')
	bit_string = ""

#	Se usa para leer linea por linea el archivo binario
	byte = file.read(1)
	contador = 1;
	while(byte != ''):
		try:
			byte = ord(byte)
			contador = contador + 1;
			print(contador)
			bits = bin(byte)[2:].rjust(8,'0')
			bit_string += bits
			byte = file.read(1)
		except:
			break

	TextEncode = quitar_bit_padding(bit_string) 
	TextDescomprimido = decodificarTexto(TextEncode)
	write_file(TextDescomprimido)

#Escribe en disco el resultado de la decodificacion, del archivo comprimido con
#los codigos de huffman.
def write_file(TextDescomprimido):

#Abrimos archivo en modo escritura si no existe se crea y si existe se sobre escribe
	file = open("matriz.txt","w")
#Escribe en el fichero los datos contenidos en la variable TexDescomprimido
	file.write(TextDescomprimido)

#Cerramos el archivo.
	file.close()


# Quita los ceros que se agregaron, cuando una cadena de bits no se completo,
#esto se hace en el archivo generar_huffman_code.
def quitar_bit_padding(encode_text):

	padding = encode_text[:8]
	paddingExtra = int(padding,2)

	encode_text = encode_text[8:]

	text = encode_text[:-1*paddingExtra]

	return text
"""
Este metodo decodifica el texto codificado con los codigos de huffman, para ello
hace uso del libro de codigos que en este caso se carga de manera interna.
"""
def decodificarTexto(TextEncode):
#genera un diccionario vacio
	tablecode = {}
	invertcode = {}

#Abrir el libro de codigos y guardar en el diccionarion.
	codes = open("codigos.txt","r")

	for i in  codes:
#Se quita el tabulador de la cadena caracteres leida.
		line = i.split("\t")

		if(line[0] == " "):
			tablecode[' '] = line[1].rstrip()
		elif(line[0]=="salto"):
			tablecode['\n'] = line[1].rstrip()
		else:
			tablecode[line[0]] = line[1].rstrip()
# Invertimos el orden del diccionario para poder  realizar la busqueda por codigos
	
	#tablecode = dict((valor ,key) for (key,valor) in tablecode.iteritems())
	
	kkey = list(tablecode.keys());
	vvalues = list(tablecode.values());
	ntablecode = {}
	for i in range(len(vvalues)):
		ntablecode[vvalues[i]] = kkey[i]
	
	tablecode = ntablecode;

	codes.close() 
	current_code = ""
	decodetext = ""
#Iteramos el texto codificado
	con = 0;
	for bit in TextEncode:
		current_code += bit
		#verifica si el codigo leido se encuentra contenido en el libro de codigos
		if (current_code in tablecode):
			con += 1;
		#Asigna a char el caracter correspondiente al codigo que se leyo.
			char = tablecode[current_code]
		#concatena cada uno de los carateres que se van encontrando
			if(con == 256):
				decodetext += char+"\n"
				con = 0;
			else:	
				decodetext += char+" "
			current_code = ""
	#retorna la cadena con el texto descomprimido.
	return decodetext

descomprimir()

print("\n\nSe ha descomprimido el archivo "+str(fichero)+" con exito!!\n")
print("El archivo descomprimido se nombro TextDescomprimido.txt\n y se guardo en la carpeta donde esta este ejecutable\n\n")
