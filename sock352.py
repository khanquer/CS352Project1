import binascii
import socket as syssock
import struct
import sys

import random

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

mainSock = (0, 0)
portTx = 0
portRx = 0
cAddress = None


fileLen = -1
maxBytes = 32000

flag = 0x00
header_len = 0x00
seqNo = 0x00
ackNo = 0x00
payloadLen = 0x00

flagsDict = {0x01:'SYN', 0x02:'FIN', 0x04:'ACK',\
         0x08:'SOCK352_RESET', 0xA0:'SOCK352_HAS_OPT'}

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
        return 
    def connect(self,address):  # fill in your code here 
        global mainSock, cAddress
        global flag, header_len, seqNo, ackNo, payloadLen
        
        print('CLIENT SOCK INFO = {}'.format(mainSock.getsockname))
        
        seqNo = random.randint(1,1000)
        
        #aflag, seqNo, ackNo, payloadLen
        
        synpackheader = self.getPacketHeader(0x01,seqNo,0x00,0x00)
        print(synpackheader)
        mainSock.sendto(synpackheader,('',portRx))
        print('SENT SYNPACK TO SERVER ')
        rec = mainSock.recv(4096)
        print('RECEIVED SYNACK PACK FROM SERVER ')
        n = self.getPacket(rec)
        return 
 
    def listen(self,backlog):
        return

    def accept(self):
        
        global mainSock        
        global flag,header_len,seqNo,ackNo,payloadLen
        print('SERVER SOCK INFO = {}'.format(mainSock.getsockname()))
        
        
        while ((flag == 0x00) and (flagsDict.get(flag)!= 'SYN')):
            rec = mainSock.recv(4096)
            [flag,header_len,seqNo,ackNo,payload_len] = self.getPacket(rec)
            print(flag)
            
        
        
        print('RECEIVED SYN PACK FROM CLIENT ')
        
        seqNo1 = random.randint(1,1000)
        flag = 0x01
        packet = self.getPacketHeader(0x01, seqNo1, seqNo+1, payloadLen)
        #vals  = [nums[0],seqNo,nums[1]+1]
        #packet = self.getPacketHeader(nums[0],seqNo,nums[1]+1)
        
        mainSock.sendto(packet,('',portRx))
        print('SENT SYNPACK TO CLIENT ')
        
        clientsocket = syssock.socket()
        
        #(clientsocket, address) = (clientsocket,cAddress)  # change this to your code 
        #return (clientsocket,address)
        return(self,portRx)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        print('SEND EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
        
        global fileLen, maxBytes
        
        if(fileLen == -1):
            longPacker = struct.Struct("!L")
            fileLen = longPacker.unpack(buffer)
            fileLen = fileLen[0]
            print(fileLen)
            mainSock.sendto(buffer,('',portRx))
            return
        print(type(buffer))
        blist = []
        print(buffer[0:maxBytes])
        for bytee in buffer:
            print('type = {}  |  val = {}'.format(type(bytee),bytee))
            blist.append(bytee)
        mainSock.sendto(buffer,('',portRx))
        bytessent = 0     # fill in your code here 
        return 1 

    def recv(self,nbytes):
    	  print('RECV EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
    	  global fileLen, maxBytes
    	  
    	  if(fileLen == -1):
    	  	   fileLenPacked = mainSock.recv(10)
    	  	   longPacker = struct.Struct("!L")
    	  	   fileLen = longPacker.unpack(fileLenPacked)
    	  	   print(fileLen[0])
    	  	   return fileLenPacked
    	  
    	  buffer = mainSock.recv(100000)
    	  #while (True):
    	  #    i = 1
    	  #bytesreceived = 0     # fill in your code here
    	  #return bytes(bytesreceived)
    	  return buffer


    def getPacketHeader(self, aflag, seqNo, ackNo, payloadLen):
        version = 0x01
        flags = aflag
        header_len= 0x00
        sequence_no = seqNo
        ack_no = ackNo
        payload_len = payloadLen
        
        head = struct.pack('bhqql',flags,header_len,seqNo,ackNo,payload_len)
        return head
        
    def getPacket(self, packet):
        l = struct.unpack('bhqql',packet)
        [flags,header_len,seqNo,ackNo,payload_len] = l
        print(l)
        return l

    def waitForPacket(self):
        global mainSock, cAddress
        print(mainSock)
        while(True):
            #(data, senderAddress) = mainSock.recvfrom(cAddress) 
            data = mainSock.recv(40)        	
            print(data)
            
            
