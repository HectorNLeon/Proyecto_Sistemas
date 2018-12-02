#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import math

#BARS
startingTime = -1
pID = 0
readyQueue = []
realMem = 2000000000
cpu=0

def tiempo(inicio):
    nt= time.time() - inicio
    return nt

def create(B):
    if startingTime == -1:
        startingTime = time.time()

    pID+=1
    pags = math.ceil(B/realMem)
    #newProc = P(pID, pags)



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()


try:
    print >>sys.stderr, 'connection from', client_address
    while True:   
        data = connection.recv(256)
        print >>sys.stderr, 'server received "%s"' % data
        if data:
            if "QuantumV" in data:
                quantum=data[9:]
            elif "RealMemory" in data:
                realMem=data[11]
            elif "SwapMemory" in data:
                swapMem=data[11]
            elif "PageSize" in data:
                pSize=data[9]
            elif "Create" in data:
                arg=data[7:]
                print arg
                create(arg)
            elif "Quantum" in data:
                print >> Quantum
            if readyQueue and cpu==0:
                Cpu
            print >>sys.stderr, 'sending answer back to the client'
            connection.sendall('process created')
        else:
            print >>sys.stderr, 'no data from', client_address
            connection.close()
            sys.exit()
            
finally:
    print >>sys.stderr, 'se fue al finally'
    connection.close()

#When communication with a client is finished, the connection needs to be cleaned up using close(). This example uses a try:finally block to ensure that close() is always called, even in the event of an error.

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))