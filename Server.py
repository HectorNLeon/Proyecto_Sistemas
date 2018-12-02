#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time

def tiempo(inicio)
    nt= time.time() - inicio
    return nt

pid=1
ready=[]
cpu=0


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
        if "QuantumV" in data:
            Quantum=data[9:]
            print Quantum
        if "RealMemory" in data:
            Rmemory=data[11]
            print Rmemory
        if "SwapMemory" in data:
            Smemory=data[11]
            print Smemory
        if "PageSize" in data:
            Psize=data[9]
            print Psize
        if "Create" in data:
            #Create
        if "Quantum" in data:
            #Quantum
        if ready and cpu==0:
            #Cpu
        if data:
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