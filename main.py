from hola import hola_f
from hola import Richford_Rice

P=(float(input('Presión de alimentación (psia): ')))
T=(float(input('Temperatura de alimentación (˚R): ')))
v_prima=float(input("v': "))
F=int(input('Flujo de alimentación (kmol/h): '))
compuestos=input('Hidrocarburos: ').split(',')
comp=input('zi: ').split(',')
print('hello world')
def h():
  a = 1
  b =3
  return a+b
hola='hola'
hola_f(hola)
Richford_Rice(F,T,P,compuestos,comp,v_prima)
