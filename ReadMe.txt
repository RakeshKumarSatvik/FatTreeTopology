In the evaluation.py line number 21, i had to change it to MN_PATH='~mininet/mininet' to make it run in my PC. Not sure if that is needed in other systems as well.

1. Did you use code from anywhere for your project? If not, say so. If so, say what functions and where they are from. (Also identify this with a comment in the
source code.) #This part is same as it wsa for ProjectB
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

For this particular project, help for Ryu was taken from internet to add and remove rules.

2. Describe the algorithm you use at the controller.
The algorithm used by me is similar to that of Global Best Fit. I try and identify the elephant flows depending on the information being sent by the sender(host). 
Step1: Identify Elephant flow.
Step2: Determine the optimal path for the particular flow.
Step3: Select the switches that need to get the new rules.
Step4: Add rules for the selected switches.
Step5: Once the elephant flow is done, remove the rules. (Commented out as it was not behaving as expected.)

Once I determine that a particular flow is an elephant flow, I try to figure out the optimal path for that particular flow (source and destination based) and send send it to the function path_poulation in my controller. This function returns the path chosen for this flow. In my design I am rerouting the elephant flows till the core switch. As we know there are four paths between a source and destination in a fat-tree topology with k=4. So i run the path evaluation between those four named straight one & two and cross one & two. 

Once I have the best path among the four paths, I determine switches that are supposed to be changed for this elephant flow. So the function named modify_path in my controller gives out the Edge, Aggregate and Core switch that is involved with this particular flow.

Once I have the switches that needs to undergo the new rules is passed on to the function add_rules in the controller. Once the new rules are added, a count is maintained to determine how many elephant flows are handled. There is a flow_id being sent from the sender(host). This is a unique flow_id for each flow irrespective of it being an elephant flow or not. This makes sure that the rules are not added over and over for the same elephant flow. Once done this flow_id is used to remove the rules (However this part is commented due to erratic behavior of the throughput!)