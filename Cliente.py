import socket
import sys
import time
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
m = ['Politicas Scheduling RR Memory LRU',
 'QuantumV 1.000',
 'RealMemory 3',
 'SwapMemory 4',
 'PageSize 1',
 (0.0, 'Create 2048'),
 (0.001, 'Create 3072'),
 (0.002, 'Create 5000'),
 (0.003, 'Address 1 4'),
 (1.0, 'Quantum'),
 (1.001, 'Address 2 1023'),
 (2.0, 'Quantum'),
 (2.001, 'Address 3 20'),
 (2.002, 'Address 3 2060'),
 (2.003, 'Create 1024'),
 (3.0, 'Quantum'),
 (3.001, 'Address 1 10'),
 (3.002, 'Fin 3'),
 (3.003, 'Create 1024'),
 (3.004, 'Create 1024'),
 (4.0, 'Quantum'),
 (4.001, 'Address 2 10'),
 (4.002, 'Address 2 3071'),
 (4.003, 'Fin 1'),
 (4.003, 'Fin 2'),
 (4.003, 'Fin 4'),
 (4.003, 'Fin 5'),
 (4.003, 'Fin 6'),
 (4.004, 'End')]
try:
    previousMsgTime = 0.0
    debug1 = False
    firstTime = True
    for i in range(5):
        print >> sys.stderr, 'client sending "%s"' % m[i]
        sock.sendall(m[i])
        respuesta = sock.recv(256)
        print >> sys.stderr, '\t\tclient received "%s"' % respuesta

    for i in range(5, len(m)):
        if firstTime:
            firstTime = False
            initialTime = time.time()
        thisMsgTime = m[i][0]
        if thisMsgTime > previousMsgTime:
            sleepTime = thisMsgTime - previousMsgTime
            if debug1:
                print >> sys.stderr, 'sleeptime', sleepTime
            time.sleep(sleepTime)
        if debug1:
            print >> sys.stderr, 'antes de calcular timedM', thisMsgTime
        print >> sys.stderr, 'client sending "%s"' % m[i][1]
        sock.sendall(m[i][1])
        respuesta = sock.recv(256)
        print >> sys.stderr, '\t\tclient received "%s"' % respuesta
        timestamp = time.time() - initialTime
        previousMsgTime = timestamp
        if debug1:
            print >> sys.stderr, 'timestamp', timestamp

    sock.close()
finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

def main(args):
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))