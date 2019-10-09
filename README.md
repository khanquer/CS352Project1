# CS352Project1
Implementation of Go-Back-N similar to TCP using UDP. This protocol is called the 352 Reliable Data Protocol (RDP) version 1 (352 RDP v1).

For part 1 of the project, your team will implement a simple go-back-N protocol similar to TCP. This
protocol is called the 352 Reliable Data Protocol (RDP) version 1 (352 RDP v1). You will realize it as a
Python (version 3) module that uses UDP as the underlying transport protocol. Later versions will add
other features like security, flow control and congestion control.
As part of the project part 1, you will be given 3 files. You can find them in the Sakai site under
"Resources" -> "Project resources" -> "Part 1" .
1. sock352.py : This is a skeleton definition of the class and methods you need to write. You
should modify this file with your implementation. That is, fill in the methods with your own code.
2. client1.py : A Python client program that uses CS 352 sockets. You may not alter the
source code for this file.
3. server1.py: A Python server program that uses CS 352 sockets. You may not alter the
source code for this file.
Your library must implement the following methods as defined in the sock352.py file, note that
some of the functions may not require you to do anything:
init(udp_port1, udp_port2)
socket()
bind(address)
connect(address)
listen(backlog)
accept()
close()
send(buffer)
recv(numBytes)
