import binascii
import socket as syssock
import struct
import sys

import random
import threading
import time

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

mainSock = (0, 0)
portTx = 0
portRx = 0
cAddress = None


fileLen = -1
maxBytes = 320

flag = 0x00
headerLen = 0x17
seqNo = 0x00
ackNo = 0x00
payloadLen = 0x00

sendable = False
bfile = bytes()

bytesreceived = 0

flagsDict = {0x01:'SYN', 0x02:'FIN', 0x03:'DATA', 0x04:'ACK',\
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
        global flag, headerLen, seqNo, ackNo, payloadLen
        
        print('CLIENT SOCK INFO = {}'.format(mainSock.getsockname))
        
        seqNo = random.randint(1,1000)
        
        #aflag, seqNo, ackNo, payloadLen
        
        synpackheader = self.getPacketHeader(0x01,seqNo,0x00,0x00)
        print(synpackheader)
        mainSock.sendto(synpackheader,('',portRx))
        print('SENT SYNPACK TO SERVER ')
        rec = mainSock.recv(4096)
        print('RECEIVED SYNACK PACK FROM SERVER ')
        [flags,headerLen,seqNo,ackNo,payloadLen] = self.openPacketHeader(rec)
       
        print(flag,headerLen,seqNo,ackNo,payloadLen)
        
        return 
 
    def listen(self,backlog):
        return

    def accept(self):
        
        global mainSock        
        global flag,headerLen,seqNo,ackNo,payloadLen
        print('SERVER SOCK INFO = {}'.format(mainSock.getsockname()))
        
        print(flag,headerLen,seqNo,ackNo,payloadLen)
        
        while ((flag == 0x00) and (flagsDict.get(flag)!= 'SYN')):
            rec = mainSock.recv(4096)
            [flag,headerLen,seqNo,ackNo,payload_len] = self.openPacketHeader(rec)
            print()
            
        print('RECEIVED SYN PACK FROM CLIENT ')
        
        seqNo1 = random.randint(1,1000)
        ackNo = seqNo+1
        flag = 0x01
        packet = self.getPacketHeader(0x01, seqNo1, ackNo, payloadLen)
        
        mainSock.sendto(packet,('',portRx))
        print('SENT SYNPACK TO CLIENT ')
        
        return(self,portRx)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        print('SEND EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
        
        global fileLen, maxBytes, sendable, bfile
        global flag, headerLen, seqNo, ackNo, payloadLen
        
        if(fileLen == -1):
            longPacker = struct.Struct("!L")
            fileLen = longPacker.unpack(buffer)
            fileLen = fileLen[0]
            print(fileLen)
            mainSock.sendto(buffer,('',portRx))
            return
            
        bytessent = 0 
        sendable = True
        print('BUFFER LEN = {}'.format(len(buffer)))
        bfile = buffer[0:len(buffer)]
        t1 = threading.Thread(target = self.sendThread)
        #t2 = threading.Thread(target = recvAckThread, args())
        
        
        t1.start()
        print('THREAD 1 STARTED')
        #t2.start()
        t1.join()
        
        
        
        return 1 

    def recv(self,nbytes):
        print('RECV EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
        global fileLen, maxBytes
        global flag, headerLen, seqNo, ackNo, payloadLen
    	  
        if(fileLen == -1):
            fileLenPacked = mainSock.recv(10)
            longPacker = struct.Struct("!L")
            fileLen = longPacker.unpack(fileLenPacked)
            print(fileLen[0])
            fileLen = fileLen[0]
            return fileLenPacked
    	  
        t2 = threading.Thread(target = self.recvThread,args = ())
        t2.start()
        t2.join()
    	  
        return 1
    
    
    #SEND PACKETS
    def sendThread(self):
        print('SEND THREAD EXECUTED')
        
        #aflag, seqNo, ackNo, payloadLen
        global fileLen, maxBytes, sendable, bfile, bytesreceived
        global flag, headerLen, seqNo, ackNo, payloadLen
        payloadLen = maxBytes-headerLen
    	  
        bytessent = 0
        startI = 0
        endI = startI + payloadLen
        while (sendable == True and bytessent < fileLen):
            if (endI > fileLen):
                endI = fileLen
                payloadLen = endI - startI
            else:
                endI = startI + payloadLen
    	      
            b = bfile[startI:endI]
            seqNo = seqNo + 1
            head = self.getPacketHeader(0x03,seqNo,0x00,payloadLen)
            sendProb = random.randint(1,10)
            if (sendProb > 4):
                mainSock.sendto(head+b,('',portRx))
                print('   SENT THIS PACKET : ')
            else:
                print('   DROPPED THIS PACKET : ')
            self.openPacketHeader(head)
            startI = startI + payloadLen
            bytessent = bytessent + payloadLen
            # fill in your code here 
        return
    
    #LISTEN FOR ACKS FROM SERVER AND 
    def recvAckThread():
        #thread1.stop
        pass
        
    #LISTEN FOR SEQ AND SEND BACK ACK 
    def recvThread(self):
        global fileLen, maxBytes, bytesreceived
        global flag, headerLen, seqNo, ackNo, payloadLen
        
    	  
        alldata = bytes()
        bytesreceived = 0
    	  
        while (True):
            hplusb = mainSock.recv(maxBytes)
            (head,data) = self.stripPacket(hplusb)
            [flags,headerLen,recseqNo,recackNo,payload_len] = self.openPacketHeader(head)
            
            if (recseqNo != seqNo): # WRONG PACKET RECEIVED (packet loss)
                print(' DROPPED PACKET   | Expected seqNo = {} | 	Received seqNo = {}'.
                              format(seqNo,recseqNo))
                print(' DROPPED PACKET   | Expected AckNo = {} | 	Received ackNo = {}'.
                              format(ackNo,recackNo))
                head = self.getPacketHeader(0x02,0x00,ackNo,payloadLen)
                mainSock.sendto(head,('',portRx))
                print('   SENT THIS ACK : ')
                self.openPacketHeader(head)
            else:
                print(' RECEIVED PACKET')
                ackNo = ackNo + 1
                head = self.getPacketHeader(0x02,0x00,ackNo,payloadLen)
                mainSock.sendto(head,('',portRx))
                print('   SENT THIS ACK  ')
                self.openPacketHeader(head)
                bytesreceived += payload_len
                alldata = alldata + data
                print(bytesreceived)
            
        pass
    	
    	
    	
    	
    	
    #aflag, seqNo, ackNo, payloadLen
    def getPacketHeader(self, aflag, seqNo, ackNo, payloadLen):
        version = 0x01
        flags = aflag
        headerLen= 0x17
        sequence_no = seqNo
        ack_no = ackNo
        payload_len = payloadLen
        
        # = 1 + 2 + 8 + 8 + 4
        head = struct.pack('!bhqql',flags,headerLen,seqNo,ackNo,payloadLen)
        
        return head
        
    def openPacketHeader(self, packet):
        l = struct.unpack('!bhqql',packet)
        [flags,headerLen,seqNo,ackNo,payload_len] = l
        print(l)
        return l
    
    def stripPacket(self, b):
        print('STRIPPING PACKET')
        d = b[1]*8 + b[2]
        print(' d = {}'.format(d))
        
        
        head = b[0:d]
        data = b[d:]
        headopen = self.openPacketHeader(head)
        print(' HEAD = {}'.format(headopen))
        print(' DATA = {}'.format(data))
        return((head,data))

            
            
