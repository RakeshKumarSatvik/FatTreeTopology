(a) How many VLANs do you have in your entire network? Whats the minimum number of VLANs you need? Why?
I have a total of 240 VLANs in my network. Every combination of a source and host is mapped to a VLAN. This helps me to determine what action needs to be taken at any given switch location in the topology depending on my VLAN ID. For example, if k = 4 and I am at Aggregate2 switch (zero indexed),and if I have a VLAN ID of 1004(h1 to h4). I can decide the next port I am supposed to send the packet to depending on the topology. The minimum number of VLANs that are needed is the number of VLANs using which you can communicate between the source and destination hosts within the topology.

(b) Show the switch FIB table for a core, aggregator, and ToR switch. Then explain and describe how you planned to setup the FIB table, and how your routing works.
Current state Information for a ToR switch is as below:
 cookie=0x0, duration=14.892s, table=0, n_packets=0, n_bytes=0, idle_age=14, priority=100,in_port=2,dl_vlan=5 actions=output:3
 cookie=0x0, duration=14.888s, table=0, n_packets=0, n_bytes=0, idle_age=14, priority=1000,in_port=4,dl_vlan=3001 actions=output:2

Current state Information for an aggregator switch is as below:
 cookie=0x0, duration=89.672s, table=0, n_packets=0, n_bytes=0, idle_age=89, priority=1000,in_port=4,dl_vlan=1002 actions=output:1
 cookie=0x0, duration=89.672s, table=0, n_packets=0, n_bytes=0, idle_age=89, priority=1000,in_port=4,dl_vlan=4003 actions=output:1

Current state Information for a core switch is as below:
 cookie=0x0, duration=364.179s, table=0, n_packets=0, n_bytes=0, idle_age=364, priority=100,in_port=4,dl_vlan=3009 actions=output:3
 cookie=0x0, duration=364.291s, table=0, n_packets=0, n_bytes=0, idle_age=364, priority=100,in_port=2,dl_vlan=1006 actions=output:2

Forwarding Table basically needs, the current state, next hop and interface. In our case, if I have reached Core0 switch and I need to go to Aggr2 switch. 
Current state   Next hop       Interface
Core0           Aggr2           Port 2

My FIB table was set as per the requirement where, given a VLAN ID and source IP I must be able send packets between any two hosts within a topology. So keeping this in mind, a rule was developed such that depending on the current state and the VLANID a next hop and its corresponding interface is chosen. Consider a FatTree topology with K = 4.

Current  interface next hop
Core0 --(1)----->  Aggr0
Core0 --(2)----->  Aggr2
Core0 --(3)----->  Aggr4
Core0 --(4)----->  Aggr6

Depending on which pod we have to reach from the core switch, we take appropriate aggregate switch and the corresponding interface!

(c) For a k=8 FatTree, how many hosts would we have? How many switches do we
have? How many paths between a pair of hosts? How many VLANs do we need?

There are (k/2)^2 hosts in each pod and there are k pods. So a total 128 hosts.
There are a total of 80 switches.
16 paths between a pair of hosts.
A total of 16256 VLANS.


Note: I am able to check the tcpdump and verify the output, but the ping.py script does not seem to be working. Tried on fixing for a long time but for no luck. The topology.py is written for a generic case whereas controller was skewed trying to get fixed for the script issues.