import binascii
import socket as syssock
import struct
import sys

import time


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

mainSock = (0, 0)
portTx = 0
portRx = 0
cAddress = None

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    print(UDPportTx)
    print(UDPportRx)
    global mainSock, portTx, portRx

    portTx = int(UDPportTx)
    portRx = int(UDPportRx)
    
    cAddress = portRx

    mainSock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    mainSock.bind(('',portTx))
    print(type(mainSock))
    pass
 
class socket:
    def __init__(self):  # fill in your code here
        print('Initializing')
        return
    def bind(self,address):
        print('Binding')
        #print(address)
        #mainSock.bind(('',1111))
        return 
    def connect(self,address):  # fill in your code here 
        global mainSock, cAddress
        print('CLIENT SOCK INFO = {}'.format(mainSock.getsockname()))
        print('ADDRESS = {}'.format(address))
        
        print('SENDING TO TEST SOCKET')
        mainSock.sendto('dlkbn'.encode('UTF-8'),('',9998))
        mainSock.sendto('dlkbn'.encode('UTF-8'),('',portRx))
        print('SENT')
        while (True):
            i = 1
        return 
 
    def listen(self,backlog):
        return

    def accept(self):
        testSocket2 = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        testSocket2.bind(('localhost',9998))
        print(testSocket2.recv(40))        
        print('RECEIVED FROM TEST SOCKET')
        
        global mainSock
        print('SERVER SOCK INFO = {}'.format(mainSock.getsockname()))
        
        print(mainSock.recv(40))
        
        #self.waitForPacket()
        clientsocket = syssock.socket()
        #(clientsocket, address) = (clientsocket,cAddress)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytessent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived

    def waitForPacket(self):
        global mainSock, cAddress
        print(mainSock)
        while(True):
            #(data, senderAddress) = mainSock.recvfrom(cAddress) 
            data = mainSock.recv(40)        	
            print(data)
            
            
