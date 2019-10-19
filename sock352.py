
import binascii
import socket as syssock
import struct
import sys

#

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    pass

version = 0x1 # have to be filled in
flags = 0 # have to be filled in
opt_ptr = 0
protocol = 0
header_len = 0 # have to be filled in
checksum = 0
source_port = 0
dest_port = 0
sequence_num = 0 # have to be filled in
ack_no = 0 # have to be filled in
window = 0
payload_len = 0 # have to be filled in
    
class socket:
    
    def __init__(self):  # fill in your code here 
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
        bytesent = 50    # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 50   # fill in your code here
        return bytesreceived 


    

