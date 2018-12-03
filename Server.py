#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import math
from tabulate import tabulate
# Definicion del objeto proceso que cuenta con un Pid, numero de paginas y 
# tabla de paridad y sus metodos de incializcion, modificacion y get’s
class Process():
    pid= int
    pages= int
    parity = []
    
    def __init__(self, pid, pages):
        self.pid = pid
        self.pages = pages
        for x in xrange(0,pages):
            self.parity.append([-1,0])
    
    def modificarP(self, page,marco, bit):
        self.parity[page] = [marco, bit]

    def __repr__(self):
        return str(self.pid)

    def __str__(self):
        return self.pid

#VARIABLES: declaración de la variables globales para el manejo la memoria, 
# cola de procesos lru, tiempo de inciio, cpu y arreglos de tablas para 
# manejar los print de tabulate,las metricas de desempeno y las visitas a paginas
startingTime = -1
pID = 0
cpu= Process(-1,1)
readyQueue = []
realMem = []
over = []
swapMem=[]
smSize=0
rmSize=0    
pSize=0
LRU = []
table=[]
started = 0
command=[]
metricas = []
pageFault = 0
temp=0
visitaP=[]
#Funcion que recibe los valores a desplegar en la tabla de tabulate para 
#agregarlos a un arreglo que se utilizara para mostrar los cambios totales 
#cuando se termine el programa(End)
def appendTable(command,timestamp,direc,readyQueue,cpu,realMem,swapMem,over):
    global table
    d = direc
    ready = []
    rm = []
    sw =[]
    o =[]
    incpu = cpu
    for i in range(0,len(readyQueue)):
        ready.append(readyQueue[i])
    for i in range(0,len(realMem)):
        rm.append(realMem[i])
    for i in range(0,len(swapMem)):
        sw.append(swapMem[i])
    for i in range(0,len(over)):
        o.append(over[i])
    table.append([command,timestamp,d,ready,incpu,rm,sw,o])


#Funcion que calcula el timeStamp a partir del tiempo incial que es cuando 
#se realiza la conexion con el cliente y se recive un proceso
def tiempo(inicio):
    nt= time.time() - inicio
    return nt

#Funcion que crea un proceso y lo carga en memoria o lo agrega a la cola de 
#listos segun sea el caso
def create(B):
    global startingTime
    global cpu
    global readyQueue
    global pID
    global pSize
    global temp


    if startingTime == -1:
        startingTime = time.time()
        started = 1
        temp = tiempo(startingTime)
        print temp

    pID = pID +1
    pags = math.ceil(B/(pSize*1024))
    pags = int(pags)
    print pags
    newProc = Process(pID, pags)
    actualTime = tiempo(startingTime)

    if cpu.pid == -1:
        cpu = newProc
        loadMem(newProc.pid,0)
    else:
        readyQueue.append(newProc)
    visitaP.append([pID,0,0,0])
    metricas.append([pID,0,actualTime,actualTime])
    owo = str(actualTime) + ": process " + str(pID) + " created " + "size " + str(pags)
    connection.sendall(owo)
    print tabulate([['Comando','timestamp','Dir. Real','Cola de listos', 'CPU','Memoria real','Area de swapping','Procesos Terminados'], [command[0], actualTime,' ', readyQueue ,cpu.pid,realMem,swapMem,over]], headers='firstrow',tablefmt='orgtbl')
    appendTable(command[0],actualTime,' ',readyQueue,cpu.pid,realMem,swapMem,over)

#Funcion para cambiar el bit de residencia y marco en el que esta 
#almacenado en el objeto proceso con el pid y num de pagina recibido
def changeParity(pid, page, frame, bit):
  global cpu
  global readyQueue
  if cpu.pid == pid:
    cpu.modificarP(page, frame, bit)
  else:
    for x in xrange(0, len(readyQueue)):
      if readyQueue[x].pid == pid:
        readyQueue[x].modificarP(page, frame, bit)

#Funcion que termina la ejecucion de un proceso y borra sus paginas de la 
#memoria 
def fin(procid):
    global cpu
    global readyQueue
    global over
    if(cpu.pid == procid):
        over.append(cpu)
        cpu = Process(-1,1)  
  
    else:
        for i in range(0,len(readyQueue)):
            if readyQueue[i].pid==procid:
                over.append(readyQueue[i])
                del readyQueue[i]
                break
    for i in range(0,len(realMem)):
        if realMem[i][0] == over[-1].pid:
            LRU.remove(realMem[i])
            realMem[i] = ['L']
    for i in range(0,len(swapMem)):
        if swapMem[i][0] == over[-1].pid:
            swapMem[i] = ['L']
    timestamp = tiempo(startingTime)
    metricas[over[-1].pid-1] = [over[-1].pid,metricas[over[-1].pid-1][1],timestamp-metricas[over[-1].pid-1][3]-metricas[over[-1].pid-1][1],timestamp-metricas[over[-1].pid-1][3]]
    if visitaP[over[-1].pid-1][1] > 0:
      visitaP[over[-1].pid-1] = [over[-1].pid,visitaP[over[-1].pid-1][1],visitaP[over[-1].pid-1][2],1-(float(visitaP[over[-1].pid-1][2])/float(visitaP[over[-1].pid-1][1]))]
    connection.sendall(str(timestamp)+" Proceso "+str(over[-1].pid)+" Terminado")

    print tabulate([['Comando','timestamp','Dir. Real','Cola de listos', 'CPU','Memoria real','Area de swapping','Procesos Terminados'], [command[0], timestamp,' ', readyQueue ,cpu.pid,realMem,swapMem,over]], headers='firstrow',tablefmt='orgtbl')
    appendTable(command[0], timestamp,' ', readyQueue,cpu.pid,realMem,swapMem,over)

#Funcion que maneja la politica de LRU para la asignacion de la memoriareal
def modifyLRU(pid, page):
  global LRU
  global rmSize
  global pSize
  if [pid, page] in LRU:
    LRU.remove([pid, page])
  if len(LRU) == int(rmSize/pSize):
    visitaP[pid-1]=[pid,visitaP[pid-1][1],visitaP[pid-1][2]+1,visitaP[pid-1][3]]
    LRU.pop(0)
  LRU.append([pid, page])


#Funcion que verifica la pagina de un proceso, si esta en memoria no hace 
#nada  y si no la carga en memoria
def address(proc, vAddr):
    global pageFault
    realLoc=0
    if proc == cpu.pid:
      page = int(vAddr/(pSize*1024))
      if page < cpu.pages:
        visitaP[cpu.pid-1] = [cpu.pid,visitaP[cpu.pid-1][1]+1,visitaP[cpu.pid-1][2],visitaP[cpu.pid-1][3]]
        if cpu.parity[page][1] == 1:
          realLoc = cpu.parity[page][0]*(pSize*1024) + vAddr % (pSize*1024)
        else:
          loadMem(proc, page)
          realLoc = cpu.parity[page][0]*(pSize*1024) + vAddr % (pSize*1024)
        answer = str(tiempo(startingTime)) + " real address: " + str(realLoc)
      else:
        answer = str(tiempo(startingTime)) + " address " + str(vAddr) + " outside of process! Se ignora"
    else:
      answer = str(tiempo(startingTime)) + " " + str(proc) + " no se está ejecutando. Se ignora"
    print tabulate([['Comando','timestamp','Dir. Real','Cola de listos', 'CPU','Memoria real','Area de swapping','Procesos Terminados'], [command[0], tiempo(startingTime), realLoc, readyQueue ,cpu.pid,realMem,swapMem,over]], headers='firstrow',tablefmt='orgtbl')
    appendTable(command[0], tiempo(startingTime), realLoc, readyQueue ,cpu.pid,realMem,swapMem,over)
    connection.sendall(answer)

#Funcion que hace los cambios respectivos en el cpu y cola de listos cuando 
#termina un ciclo del quantum segun el RR
def quantum():
  global cpu
  global readyQueue
  global temp
  indexN= 0
  t= tiempo(startingTime)
  metricas[cpu.pid-1] = [cpu.pid, (t-temp)+metricas[cpu.pid-1][1],0,metricas[cpu.pid-1][3]]
  temp = t
  readyQueue.append(cpu)
  cpu= readyQueue.pop(0)
  for x in range(0,smSize):
    if cpu.pid == swapMem[x][0]:
      indexN= x
      break
  if indexN != 0:
    loadMem(swapMem[indexN][0], swapMem[indexN][1])
  else:
    loadMem(cpu.pid,0)
  visitaP[cpu.pid-1] = [cpu.pid,visitaP[cpu.pid-1][1]+1,visitaP[cpu.pid-1][2],visitaP[cpu.pid-1][3]]
  t= tiempo(startingTime)
  res= str(t) + ' quantum end.'
  print tabulate([['Comando','timestamp','Dir. Real','Cola de listos', 'CPU','Memoria real','Area de swapping','Procesos Terminados'], [command[0], t, ' ', readyQueue ,cpu.pid,realMem,swapMem,over]], headers='firstrow',tablefmt='orgtbl')
  appendTable(command[0], t, ' ', readyQueue ,cpu.pid,realMem,swapMem,over)
  connection.sendall(res)
                    

#Funcion que se encarga de manejar todas los operaciones tanto en la 
#memoria real, como en la tabla de swapping y utilizar la politica LRU
def loadMem(pid,page):
  global realMem
  global swapMem
  memFull= ['L'] not in realMem
  if [pid,page] in swapMem:
    indexY= swapMem.index([pid,page])
    swapMem[indexY]= ['L']
  if not memFull:
    indexL= realMem.index(['L'])
    realMem[indexL]= [pid,page]
    changeParity(pid,page,indexL,1)
    modifyLRU(pid,page)
  else:
    if ['L'] in swapMem:
      indexSw= swapMem.index(['L'])
    else:
      indexSw= 0
    indexMV= realMem.index(LRU[0])
    swapMem[indexSw]= realMem[indexMV]
    changeParity(realMem[indexMV][0],realMem[indexMV][1],-1,0)
    realMem[indexMV]= [pid,page]
    changeParity(pid,page,indexMV,1)
    modifyLRU(pid,page)

#Funcion que despliega la tabla final cuando se recibe el END
def end():
    promedioT =0
    promedioE =0
    glV=0
    glPF=0
    print tabulate(table, headers=['Comando','timestamp','Dir. Real','Cola de listos', 'CPU','Memoria real','Area de swapping','Procesos Terminados'],tablefmt='orgtbl')
    print ''
    print tabulate(metricas, headers=['Proceso','Tiempo de CPU','Tiempo de Espera','Turnaround'],tablefmt='orgtbl')
    for i in range(0,len(metricas)):
      promedioT +=metricas[i][3]
      promedioE +=metricas[i][2]
    promedioT = promedioT/len(metricas)
    promedioE = promedioE/len(metricas)
    print tabulate([['Promedio Tiempo de Espera','Promedio Turnaroound'],[promedioE, promedioT]], headers=['firstrow'],tablefmt='orgtbl')
    print tabulate(visitaP, headers=['Proceso','Visita de Paginas','Page Faults','Rendimiento'],tablefmt='orgtbl')
    for i in range(0,len(visitaP)):
      glV +=visitaP[i][1]
      glPF +=visitaP[i][2]
    glR= 1-(float(glPF)/float(glV))
    print tabulate([['Visita de Paginas Total','Page Faults Total','Rendimiento Total'],[glV, glPF,glR]], headers=['firstrow'],tablefmt='orgtbl')
    connection.sendall(' ')
                  
#Declaracion y asignacion del socket para la conexion
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)
connection, client_address = sock.accept()

n=0
try:
    while True:
        data = connection.recv(256)
        i=0
        x=0
        #Validacion para poder recibir varios comandos en al mismo tiemp
        if n > 4:
            while i < len(data)-1:
                command.append(data[i])
                i+=1
                while i <= (len(data)-1) and not data[i].isupper():
                    command[x]+=data[i]
                    i+=1
                x+=1
        else:
            command.append(data)
        n+=1
        if data:
            while command:
                print command[0]
                #Validaciones que permiten recibir los comandos del cliente 
                if "Politicas Scheduling" in command[0]:
                    command.pop(0)
                    connection.sendall(' ')
                elif "QuantumV" in command[0]:
                    qu=float(command[0][9:])
                    command.pop(0)
                    connection.sendall(' ')
                elif "RealMemory" in command[0]:
                    rmSize=int(command[0][11])
                    for i in range(0,rmSize):
                        realMem.append(['L'])
                    command.pop(0)
                    connection.sendall(' ')
                elif "SwapMemory" in command[0]:
                    smSize=int(command[0][11])
                    for i in range(0,smSize):
                        swapMem.append(['L'])
                    command.pop(0)
                    connection.sendall(' ')
                elif "PageSize" in command[0]:
                    pSize=int(command[0][9])
                    command.pop(0)
                    connection.sendall(' ')
                elif "Create" in command[0]:
                    arg=int(command[0][7:])
                    create(arg)
                    command.pop(0)
                elif "Address" in command[0]:
                    arg = command[0].split()
                    address(int(arg[1]), int(arg[2]))
                    command.pop(0)
                elif "Quantum" in command[0]:
                    if cpu.pid != -1:
                      quantum()
                    else:
                        t= tiempo(startingTime)
                        res= repr(t) + ' quantum end. CPU vacia. Se ignora'
                        connection.sendall(res)  
                    command.pop(0)   
                elif "Fin" in command[0]:
                  arg=int(command[0][4:])
                  fin(arg)
                  command.pop(0)
                elif "End" in command[0]:
                  end()
                  command.pop(0)
        else:
            connection.close()
            sys.exit()
            
finally:
    connection.close()

#When communication with a client is finished, the connection needs to be cleaned up using close(). This example uses a try:finally block to ensure that close() is always called, even in the event of an error.

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))