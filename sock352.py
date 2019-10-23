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
maxBytes = 300
gstartI = 0
done = False

timeoutDuration = 0.2
startChanged = False

flag = 0x00
headerLen = 0x17
firstseqNo = 0x00

seqNo = 0x00
ackNo = 0x00
reqackNo = 0x00  #received ackNo
payloadLen = 0x00


bfile = bytes()
alldata = bytes()

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
        [flags,headerLen,s,a,payloadLen] = self.openPacketHeader(rec)
        ackNo = s
        
        print( ' CLIENT SEQNO = {}  |  ACKNO = {}  '.format(seqNo,ackNo))
        
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
            [flag,headerLen,s,a,payload_len] = self.openPacketHeader(rec)
            print()
            
        print('RECEIVED SYN PACK FROM CLIENT ')
        
        seqNo = random.randint(1,1000)
        ackNo = s+1
        packet = self.getPacketHeader(0x01, seqNo, ackNo, payloadLen)
        
        mainSock.sendto(packet,('',portRx))
        print('SENT SYNPACK TO CLIENT ')
        
        print( ' SERVER SEQNO = {}  |  ACKNO = {}  '.format(seqNo,ackNo))
        return(self,portRx)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        print('SEND EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
        
        global fileLen, maxBytes, bfile, firstseqNo
        global flag, headerLen, seqNo, ackNo, payloadLen
        
        if(fileLen == -1):
            longPacker = struct.Struct("!L")
            fileLen = longPacker.unpack(buffer)
            fileLen = fileLen[0]
            print(fileLen)
            mainSock.sendto(buffer,('',portRx))
            return
            
        firstseqNo = seqNo + 1
        bytessent = 0 
        print('BUFFER LEN = {}'.format(len(buffer)))
        bfile = buffer[0:len(buffer)]
        t1 = threading.Thread(target = self.sendThread)
        t3 = threading.Thread(target = self.recvAckThread)
        #t2 = threading.Thread(target = recvAckThread, args())
        
        
        print('THREAD 1 STARTED')
        t1.start()
        print('THREAD 3 STARTED')
        t3.start()
        t1.join()
        t3.join()        
        
        
        return 1 

    def recv(self,nbytes):
        print('RECV EXECUTED \n\t SOCK INFO : {}'.format(mainSock.getsockname()))
        global fileLen, maxBytes
        global flag, headerLen, seqNo, ackNo, payloadLen
    	  
        if(fileLen == -1):
            fileLenPacked = mainSock.recv(10)
            longPacker = struct.Struct("!L")
            fileLen = longPacker.unpack(fileLenPacked)
            print('FILE LENGTH = {}'.format(fileLen[0]))
            fileLen = fileLen[0]
            return fileLenPacked
    	  
        t2 = threading.Thread(target = self.recvThread,args = ())
        t2.start()
        t2.join()
    	  
        return alldata
    
    
    #SEND PACKETS
    def sendThread(self):
        print('SEND THREAD EXECUTED')
        
        #aflag, seqNo, ackNo, payloadLen
        global fileLen, maxBytes, bfile, bytesreceived, gstartI, done, startChanged
        global flag, headerLen, seqNo, ackNo, payloadLen
        payloadLen = maxBytes-headerLen
    	  
        bytessent = 0
        startI = 0
        endI = startI + payloadLen
        while(done == False):
            if (startI < fileLen):
                if (endI > fileLen):
                    endI = fileLen
                    payloadLen = endI - startI
                else:
                    endI = startI + payloadLen
    	      
                b = bfile[startI:endI]
                seqNo = seqNo + 1
                head = self.getPacketHeader(0x03,seqNo,0x00,payloadLen)
                sendProb = random.randint(1,10)
                #mainSock.sendto(head+b,('',portRx))
                
                if (sendProb > 2):
                    mainSock.sendto(head+b,('',portRx))
                    print('   SENT THIS PACKET : ')
                else:
                    print('   DROPPED THIS PACKET : ')
                
                #print('   SENT THIS PACKET : ')
                self.openPacketHeader(head)
                print('\t INDICES | startI = {} | endI = {}'.format(startI,endI))
                if (startChanged == True):
                    startI = gstartI
                else: 
                    startI = startI + payloadLen
                startChanged = False
                bytessent = bytessent + payloadLen
                # fill in your code here 
            else:
                print(startI,startChanged,gstartI)
                if(startChanged == True):
                    startI = gstartI
                time.sleep(3)
        return
    
    #LISTEN FOR ACKS FROM SERVER AND 
    def recvAckThread(self):
        global firstseqNo, timeoutDuration, gstartI, done
        
        currentackNo = firstseqNo
        startTime = 0
        endTime = 0
        startTime = time.clock()
        mainSock.settimeout(2)
        while(not done):
            print('recvacklistening')
            
            try:
                hplusb = mainSock.recv(maxBytes)
            except syssock.timeout:
                print('SOCKET TIMEOUT BUT CONTINUE')
                
            
            (head,data) = self.stripPacket(hplusb)
            print('\n \t\t PACKET  ACK THAT WAS RECEIVED')
            [flags,headerLen,recseqNo,recackNo,payload_len] = self.openPacketHeader(head)
            print(' \t\t CLIENT THREAD 2 \n| seqNo = {} | ackNo = {} | recseqNo = {} | recackNo = {} | currackNo = {} \n'
                      .format(seqNo,ackNo,recseqNo,recackNo,currentackNo))
            if (recackNo > currentackNo):
                startTime = time.clock()
                currentackNo = recackNo
            endTime = time.clock()
            print(time.clock())
            dt = endTime - startTime
            print(' dt = {}'.format(dt))
            if (dt > 0.01): #NEED TO TIME OUT AND RESET SENDER
                print('TIME OUT SEND THE FUCKING PACKET')
                gstartI = (currentackNo - firstseqNo)*maxBytes
                print('\t\t gstartI = {}  | start is CHANGED '.format(gstartI))
                startChanged = True
                            
            numpackets = (currentackNo - firstseqNo)
            print('\t NUMBER OF PACKETS SENT (ACK RECEIVED) = {}'.format(numpackets))
            print('\t\t {}'.format(numpackets*maxBytes))
            if (numpackets*maxBytes > fileLen):
                done = True
        pass
        
    #LISTEN FOR SEQ AND SEND BACK ACK 
    def recvThread(self):
        global fileLen, maxBytes, bytesreceived, done, alldata
        global flag, headerLen, seqNo, ackNo, payloadLen
        
    	  
        #alldata = bytes()
        bytesreceived = 0
    	  
        while (not done):
            hplusb = mainSock.recv(maxBytes)
            (head,data) = self.stripPacket(hplusb)
            print('\nPACKET THAT WAS RECEIVED')
            [flags,headerLen,recseqNo,recackNo,payload_len] = self.openPacketHeader(head)
            
            if (recseqNo != ackNo): # WRONG PACKET RECEIVED (packet loss)
                print(' DROPPED PACKET   | Expected seqNo = {} | 	Received seqNo = {}'.
                              format(seqNo,recseqNo))
                print(' DROPPED PACKET   | Expected AckNo = {} | 	Received ackNo = {}'.
                              format(ackNo,recackNo))
                head = self.getPacketHeader(0x02,0x00,ackNo,payloadLen)
                mainSock.sendto(head,('',portRx))
                print('   SENT THIS ACK : ')
                self.openPacketHeader(head)
            else:
                print(' RECEIVED CORRECT PACKET')
                ackNo = ackNo + 1
                head = self.getPacketHeader(0x02,0x00,ackNo,payloadLen)
                mainSock.sendto(head,('',portRx))
                print('   SENT THIS ACK  ')
                self.openPacketHeader(head)
                bytesreceived += payload_len
                alldata = alldata + data
                print(bytesreceived)
            
            if (bytesreceived >= fileLen):
                done = True
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
        #print(' d = {}'.format(d))
        
        head = b[0:d]
        data = b[d:]
        headopen = self.openPacketHeader(head)
        print(' HEAD = {}'.format(headopen))
        print(' DATA = {}'.format(data))
        return((head,data))

            
            
