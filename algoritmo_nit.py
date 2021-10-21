import re

try:
	og_nit = input("NIT")

	#Solo son 4 comandos pero parece ser demasiado
	_nit = og_nit.replace('-','')
	_nit = _nit.upper()
	_nit = _nit[::-1]
	_nit = list(_nit)
	
	multiplier = 2
	sigma = 0

	#Paso 1 y 2
	for i in range(1, len(_nit)):
		if i%6 == 0:
			print(int(_nit[i])*multiplier)
			sigma += int(_nit[i])*multiplier
			multiplier = 2
		else:
			print(int(_nit[i])*multiplier)
			sigma += int(_nit[i])*multiplier
			multiplier += 1
	#Paso 3
	print("Sumatoria: ",sigma)
	#Paso 4 y 5
	modulo_once = 11 - sigma%11
	print(modulo_once, " : ", _nit[0])

	#Verificación
	if modulo_once == int(_nit[0]):
		print("El nit {} es válido".format(og_nit))
	elif modulo_once == 10 and _nit[0] == 'K':
		print("El nit {} es válido".format(og_nit))
	else:
		print("NIT NO VALIDO")
except Exception as e:
	raise e

sub_cadena = re.findall(r"\d\d\/\d\d\/\d\d\d\d", "24/12/1998")
print(sub_cadena[0])
sub_cadena = re.findall(r"\d\d\:\d\d", "00:47")
print(sub_cadena[0])