CS 352 Fall 2019 Programming 
Project Part 1
Imrhankhan Shajahan, Anagh Telluri
Python Version: 3.6.8
Problem:
For part 1 of the project, your team will implement a simple go-back-N protocol similar to TCP. This protocol is called the 352 Reliable Data Protocol (RDP) version 1 (352 RDP v1). You will realize it as a Python (version 3) module that uses UDP as the underlying transport protocol.

Algorithm:
Setting up the connection
Client sends a SYN message to the Server
Sequence number set to x(random number)
The server responds with a SYN-ACK message 
Sequence number is set to y(random number)
Acknowledgement number is set to x+1(x being the sequence number received from client)
The client receives the SYN-ACK message and sends its own SYN-ACK message
Sequence number = x+1
Acknowledgement number is set to y+1(y being the sequence number received from server)
Sending the data
First the client sends the file length to the server
Next, the first thread is started, on which the client sends the file contents to the server
If the file size is bigger than the maximum packet size, then the file is broken up into segments, where each segment is less than or equal to the maximum packet size
If the file size is smaller than the maximum packet size, it is sent in one packet
In both cases when a segment of the file is sent, it is sent along with the header
The segment is appended to the header
The 3rd thread is also started when the data starts sending. It is responsible for receiving acknowledgements and detecting timeouts
This thread sets the correct sequence number of the next expected one
If a timeout is detected in the ACK’s being sent back, the start index is shifted back(calculated using required ACK and maxSendable)
The startI is reset in the main loop for sending
Receiving the data
When the data comes to the server, its in the format (header + data), so we call stripPacket() to get the result (header, data) as a tuple
It checks if the received sequence number is equal to the acknowledgement number to be sent
If it isn’t, then the server sends the required Sequence number to be sent by the client
If it is in the proper order, Acknowledgement number increments by 1 and the server sends an acknowledgement to the client
Closing
Both attempt to send FIN packets. The one that receives it first becomes host 2 and the other becomes host 1. 
Host 1 sends a FIN message, then host 2 sends an ACK message and a FIN message, finally, host 1 sends the ACK message and the connection is closed
Variables:
maxBytes = 32000: maximum UDP packet size
maxSend: maxBytes-headerLen. The max number of bytes sent per packet
gstartI: global start to sync with the send method when the thread times out
gseqno: global sequence number to sync with the send method when the thread times out
showPrint: enables or disables printing depending on value(True or False)
dropPackets: Boolean telling the program to drop packets or not
bfile: the file contents. This variable is used in sending
alldata: the data that is being received. It is changed in the recvThread method. Everytime that data is sent, It adds the sent content to alldata. After the receiving thread is done, the recv method finally returns alldata
flagsDict = {0x01: ‘SYN’, 0x02: ‘FIN’, 0x03: ‘DATA’, 0x04: ‘ACK’, 0x08: ‘SOCK352_RESET’, 0xA0: ‘SOCK352_HAS_OPT’}: dictionary of flags to make it easier to use the flags and their respective bits
