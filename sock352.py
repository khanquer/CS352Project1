
import binascii
import socket as syssock
import struct
import sys

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

portTx = 0
portRx = 0

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
	print(UDPportTx)
	print(UDPportRx)
	
	portTx = UDPportTx
	portRx = UDPportRx	
	pass
    
class socket:
    
    def __init__(self):  # fill in your code here 
        self.sock = syssock.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return
    
    def bind(self,address):
        return 

    def connect(self,address):  # fill in your code here 
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 


    

