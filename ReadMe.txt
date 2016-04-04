1. Did you use code from anywhere for your project? If not, say so. If so, say what functions and where they are from. (Also identify this with a comment in the
source code.)
I have used several online sources for parts of my code, mainly the ones discussed in Piazza. 
In sender.c
-> I used this link to get the ip address: http://stackoverflow.com/questions/4139405/how-can-i-get-to-know-the-ip-address-for-interfaces-in-c
-> For the basic sending and receiving purposes of a socket, I used this as my reference http://www.thegeekstuff.com/2011/12/c-socket-programming/

In receiver.c
-> I used this link to get the ip address: http://stackoverflow.com/questions/4139405/how-can-i-get-to-know-the-ip-address-for-interfaces-in-c
-> For the basic sending and receiving purposes of a socket, I used this as my reference http://www.thegeekstuff.com/2011/12/c-socket-programming/
-> I used this website to understand how to use the select() function, http://developerweb.net/viewtopic.php?id=2933

In hedera_controller.py
-> I used this website to understand socket programming in python, http://www.tutorialspoint.com/python/python_networking.htm

The basic max and min function was looked up in the internet. For the purpose of the file read, I have used a part of the code I had used in my previous projects.
For small transactions and definitions of function, man page was referred as and when required.

2. Describe how you implement the sender and receiver at hosts
Sender:
In my sender.c:
I first create a new thread to get the get_flow_state function which acts as a server and is listening to the port for a request from the controller. Once the socket receives request from controller, appropriate measures can be taken as a part of the next part of project.

After the thread is spawned off, in my main thread I have created another function called command_parser() as given in the requirement which basically reads the information from the file given as input. This file has the informatin regarding the destination IP, port number and number of bytes that is supposed to be sent.Once we have these information we can create a socket and populate it to that information read from the file. Now, depending on the size of transmission requested by the file I populate a random buffer and transmit it through the socket. This is looped over until I transmit it to all the destinations pointed out by the trace file. As and when I reach the EOF for trace file, it exits the loop and waits for the thread that was created initially and the program is exited once the pthread_join() is successful. (In our case the join wont be successful as the get_flow_state() runs forever). Sockopt of SO_REUSEPORT is used to reuse the ports.

In my receiver.c:
I have created another function in this file called command_parser() as given in the requirement which basically reads the information from the file given as input. In this input file the information about the port numbers the host is supposed to listen is given. This loops until the end of file so that so sockets are created for each of the port number given by the input file.

The receiver basically acts as a server where he creates a socket for the port numbers mentioned in the input file. Once the socketfd is created, he binds it and listens to that particular fd. Since there will be more than one host who tries to send packets to this host, we need to use a select function which helps the selection of sockets to listen to. The logic behind this select operation is basically that there are two sets created, first the set is populated with all the socketfds created. Once the entire input file is read, this set is copied on to a temporary set. Now, select function is made to wait for any activity in any of that temporary set. Once select returns stating that there was some activity, there is a loop which loops for the number of times there were number of ports mentioned in the input file. There is a check to make sure if there was an activity in each of them using FD_ISSET() which tells us that if there was any activity in that. Once we get the fd which is receiving information, we populate it to the first set which has connect fd and is now has the accept fd as well. the next important thing is to clear this fd from the temporary set. So once this is done, we loop around this set which has both socketfd and connfd for receiving information from that particular fd. (There is a memcpy at the beginning which makes sure that both the sets have the same information). This basically helps in reading from multiple sources and port numbers. Sockopt of SO_REUSEPORT is used to reuse the ports.

3. Describe the algorithm you use at the controller.
In the controller algorithm, it is basically divided into three categories. Edge, Aggregate and Core switches.
Edge Switches:
If the destination corresponds to one of the two hosts connected to the Edge switch then the traffic is transferred to the appropriate port, as we are aware of the port and host connection. If there is any other scenario, then the packets are transferred above with ECMP with equal weight to both the ports.

Aggregate Switches:
If the destination corresponds to one of the four hosts connected to the Edge switch then the traffic is transferred to the appropriate port, as we are aware of the port and host connection. If there is any other scenario, then the packets are transferred above with ECMP with equal weight to both the ports.

Core Switches:
Once we know the destination in the core switches, we can navigate the traffic to appropriate aggreagete switches. Once the aggregate switch receives information for one of its destined hosts, then the traffic is transferred to the appropriate Edge switch and thereby deliviering it to the end host.